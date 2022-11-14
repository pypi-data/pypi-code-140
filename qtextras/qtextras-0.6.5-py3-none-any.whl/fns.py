from __future__ import annotations

import argparse
import ast
import multiprocessing as mp
import re
import typing as t
from argparse import Namespace
from contextlib import contextmanager
from pathlib import Path
from warnings import warn

import pandas as pd
import pyqtgraph as pg
from pyqtgraph.parametertree import Parameter, ParameterTree
from pyqtgraph.Qt import QT_LIB, QtCore, QtGui, QtWidgets

# -----
# For ruamel yaml
# -----
# Needed for external modules to catch a YamlError
from ruamel.yaml import YAML, YAMLError  # noqa

from qtextras.typeoverloads import FilePath

# -----
# For Pyyaml
# -----
# import yaml
# from yaml import YAMLError
# loader = yaml.UnsafeLoader
# dumper = yaml.Dumper
# def yamlLoad(stream):
#   return yaml.load(stream, loader)
# def yamlDump(data, stream):
#   return yaml.dump(data, stream, dumper, sort_keys=False)

dumper = YAML()
loader = YAML(typ="safe")


def _representColor(representer, color: QtGui.QColor):
    return representer.represent_list(color.getRgb())


# Register some types to the YAML representer since their states don't get serialized
# properly
dumper.representer.add_representer(QtGui.QColor, _representColor)


def yamlLoad(stream):
    return loader.load(stream)


def yamlDump(data, stream):
    return dumper.dump(data, stream)


def multiprocessApply(
    func,
    iterLst,
    descr="",
    iterArgPos=0,
    extraArgs=(),
    showProgress=None,
    applyAsync=True,
    total=None,
    pool=None,
    processes=None,
    debug=False,
    discardReturnValues=False,
    **extraKwargs,
):
    # Define tqdm here to avoid warnings below. If ``showProgress`` is False
    # then tqdm is not used so this is safe.
    tqdm = None
    from importlib import util

    tqdmExists = util.find_spec("tqdm") is not None
    if showProgress is None:
        showProgress = tqdmExists
    if showProgress and not tqdmExists:
        raise ModuleNotFoundError("Cannot show progress without the `tqdm` module")
    elif showProgress:
        from tqdm import tqdm as tqdm

    if total is None:
        try:
            total = len(iterLst)
        except (AttributeError, TypeError):
            total = None

    callback = None
    if showProgress and applyAsync and not debug:
        progBar = tqdm(total=total, desc=descr)

        def updateProgBar(*_):
            progBar.update()

        callback = updateProgBar
    elif showProgress:
        iterLst = tqdm(iterLst, total=total, desc=descr)

    pre_results = []
    errs = {}

    def errCallback(fnArgs, ex):
        errs[str(fnArgs[iterArgPos])] = str(ex)

    if debug:

        def applyFunc(func_, args):
            return func_(*args, **extraKwargs)

    else:
        if pool is None:
            pool = mp.Pool(processes)
        if applyAsync:

            def applyFunc(func_, args):
                return pool.apply_async(
                    func_,
                    args,
                    kwds=extraKwargs,
                    callback=callback,
                    error_callback=lambda ex: errCallback(args, ex),
                )

        else:
            applyFunc = pool.apply

    extraArgs = tuple(extraArgs)
    for el in iterLst:
        curArgs = extraArgs[:iterArgPos] + (el,) + extraArgs[iterArgPos:]
        pre_results.append(applyFunc(func, curArgs))
    if not debug:
        pool.close()
        pool.join()
    if len(errs) > 0:
        msg = ["The following errors occurred at the specified list indices:"]
        for k, v in errs.items():
            msg.append(f"{k}: {v}")
        warn("\n".join(msg))
    if discardReturnValues:
        return
    if applyAsync and not debug:
        return [res.get() for res in pre_results]
    else:
        return pre_results


def dynamicDocstring(embed=False, **kwargs):
    """
    Docstrings must be known at compile time. However this prevents expressions like

    ```
    x = ['dog', 'cat', 'squirrel']
    def a(animal: str):
      \"\"\"
      param animal: must be one of {x}
      \"\"\"
    ```

    from compiling. This can make some features of function registration difficult,
    like dynamically generating limits for a docstring list. `dynamicDocstring` wraps
    a docstring and provides kwargs for string formatting. Retrieved from
    https://stackoverflow.com/a/10308363/9463643

    Parameters
    ----------
    embed
        Sometimes, the value that should be accessed from the docstring is not
        recoverable from its string representation. YAML knows how to serialize the
        default types, but it is a pain to write a deserialization protocol for every
        object used as a dynamic reference. To avoid this, `embed` determines whether a
        `__docObjs__` reference should eb attached to the function with the raw object
        values. I.e. instead of storing the string representation of a list kwarg,
        __docObjs__ would hold a reference to the list itself.
    **kwargs
        List of kwargs to pass to formatted docstring
    """

    def wrapper(obj):
        obj.__doc__ = obj.__doc__.format(**kwargs)
        if embed:
            obj.__docObjs__ = kwargs
        return obj

    return wrapper


def seriesAsFrame(ser: pd.Series):
    return ser.to_frame().T


def createAndAddMenuAct(
    mainWin: QtWidgets.QWidget, parentMenu: QtWidgets.QMenu, title: str, asMenu=False
) -> t.Union[QtWidgets.QMenu, QtGui.QAction]:
    menu = None
    if asMenu:
        menu = QtWidgets.QMenu(title, mainWin)
        act = menu.menuAction()
    else:
        act = QtGui.QAction(title)
    parentMenu.addAction(act)
    if asMenu:
        return menu
    else:
        return act


def pascalCaseToTitle(name: str, addSpaces=True) -> str:
    """
    Helper utility to turn a PascalCase name to a 'Title Case' title

    Parameters
    ----------
    name
        camel-cased name
    addSpaces
        Whether to add spaces in the final result

    Returns
    -------
    str
        Space-separated, properly capitalized version of ``name``
    """
    if not name:
        return name
    # changeROIImage -> change ROI Image
    # HTTPServer -> HTTP Server
    # exportData -> export Data
    name = re.sub(r"([A-Z]?[a-z0-9]+)", r" \1 ", name)
    name = name.replace("_", " ")
    # title() would turn HTTPS -> Https which we don't want
    parts = [p[0].upper() + p[1:] for p in name.split()]
    joiner = " " if addSpaces else ""
    return joiner.join(parts)


# Make a class for reference persistence
_nameFmtType = t.Callable[[str], str]


class NameFormatter:
    def __init__(self, formatter: t.Callable[[str], str] = pascalCaseToTitle):
        self._formatter = formatter

    def __call__(self, inStr: str):
        return self._formatter(inStr)

    @contextmanager
    def set(self, nameFmt: _nameFmtType):
        oldFmt = self._formatter
        self._formatter = nameFmt
        yield
        self._formatter = oldFmt


nameFormatter = NameFormatter()


def saveToFile(saveObj, savePath: FilePath):
    with open(savePath, "w") as saveFile:
        yamlDump(saveObj, saveFile)


def attemptFileLoad(
    fpath: FilePath, openMode="r", missingOk=False
) -> dict | bytes | None:
    if not Path(fpath).exists() and missingOk:
        return None
    with open(fpath, openMode) as ifile:
        loadObj = yamlLoad(ifile)
    return loadObj


def clearUnwantedParameterValues(parameterState: dict):
    for _k, child in parameterState.get("children", {}).items():
        clearUnwantedParameterValues(child)
    if parameterState.get("value", True) is None:
        parameterState.pop("value")


class _IGNORE_VALUE:
    """
    Used as a sentinel during ``fns.parameterValues`` that a parameter should be
    ignored during loading
    """


def valueIsNotDefault(parameter):
    """
    Convenience function to pass to ``parameterValues`` as a ``valueFilter`` without
    needing to specify a lambda function
    """
    return not parameter.valueIsDefault()


def parameterValues(
    parameter: Parameter,
    valueFilter: t.Callable[[Parameter], bool | t.Any] = None,
    value="value",
    groupTypes: t.Sequence[str] = ("group","_actiongroup"),
) -> t.Any | dict[str, t.Any]:
    """
    Returns just parameter values in a human-readable fashion. A group parameter's
    value is considered to be a dict of its children values. Child values are made
    serializable through ``child.saveState()["value"]``.

    Parameters
    ----------
    parameter
        The parameter to get values from. Intended to be a group parameter
    valueFilter
        Callable that returns ``True`` if a parameter should be included in the
        returned dict. If ``None``, all parameters are included.
    value:
        The type of value to retrieve. For example, it can be set to "enabled" to retrieve
        the enabled state of a parameter
    groupTypes
        The types of parameters that should be considered groups when deciding whether to
        recurse into them
    """
    returnValueOnly = parameter.type() not in groupTypes
    # Some values are not well represented as text, so call 'saveState' to ensure
    # they work
    if returnValueOnly and (not valueFilter or valueFilter(parameter)):
        return parameter.saveState()[value]
    elif returnValueOnly:
        return _IGNORE_VALUE
    # Else is a group parameter
    outDict = {}
    for child in parameter:
        isGroup = child.type() in groupTypes
        chState = parameterValues(child, valueFilter, value, groupTypes)
        if (chState is _IGNORE_VALUE) or (isGroup and not chState):
            # Don't include empty groups or ignored child values
            continue
        outDict[child.name()] = chState
    return outDict


def parameterDictWithOpts(
    param: Parameter,
    addList: t.List[str] = None,
    addTo: t.List[t.Type[Parameter]] = None,
    removeList: t.List[str] = None,
) -> dict:
    """
    Allows customized alterations to which portions of a pyqtgraph parameter will be
    saved in the export. The default option only allows saving all or no extra options.
    This allows you to specify which options should be saved, and what parameter types
    they should be saved for.

    Parameters
    ----------
    param
        The initial parameter whose export should be modified
    addList
        Options to include in the export for *addTo* type parameters
    addTo
        Which parameter types should get these options
    removeList
        Options to exclude in the export for *addTo* type parameters

    Returns
    -------
    dict
        Modified version of ``paramDict`` with alterations as explained above
    """
    if addList is None:
        addList = []
    if addTo is None:
        addTo = []
    if removeList is None:
        removeList = []

    def addCustomOpts(dictRoot, paramRoot: Parameter):
        for pChild in paramRoot:
            dChild = dictRoot["children"][pChild.name()]
            addCustomOpts(dChild, pChild)
        if type(paramRoot) in addTo:
            for opt in addList:
                if opt in paramRoot.opts:
                    dictRoot[opt] = paramRoot.opts[opt]
        for opt in removeList:
            if dictRoot.get(opt, True) is None:
                dictRoot.pop(opt)

    paramDict = param.saveState("user")
    addCustomOpts(paramDict, param)
    return paramDict


def applyParameterOpts(parameter: Parameter, opts: dict):
    """
    Applies `opts` to `param` recursively. Used in place of pyqtgraph's
    implementation due to method connection errors
    """
    state = opts.copy()
    childStates = state.pop("children", [])
    if isinstance(childStates, list):
        cs = {child["name"]: child for child in childStates}
        childStates = cs
    parameter.setOpts(**opts)
    for chName, chDict in childStates.items():
        if chName in parameter.names:
            applyParameterOpts(parameter.child(chName), chDict)


def flattenedParameters(parameter: Parameter, groupTypes: t.Sequence[str] = ("group",)):
    addList = []
    if parameter.type() in groupTypes:
        for child in parameter.children():  # type: Parameter
            addList.extend(flattenedParameters(child, groupTypes))
    else:
        addList.append(parameter)
    return addList


def flexibleParameterTree(
    treeParameters: t.Union[t.List[Parameter], Parameter] = None,
    showTop=True,
    setTooltips=True,
    resizeNameCol=True,
):
    tree = ParameterTree()
    tree.setTextElideMode(QtCore.Qt.TextElideMode.ElideRight)
    tree.header().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
    if isinstance(treeParameters, Parameter):
        treeParameters = [treeParameters]
    if not treeParameters:
        treeParameters = []
    # pyqtgraph bug: If tree isn't explicitly cleared, the invisible root isn't
    # configured correctly
    for param in treeParameters:
        tree.addParameters(param, showTop=showTop)

    # def hookupSignals(p: Parameter):
    #   for ch in p:
    #     hookupSignals(ch)
    # Make wrapper out here to avoid lambda in loop scoping issues
    def hookupWrapper(_param):
        def maybeUpdateTips(_param, change):
            desc = change[0][1]
            if "added" in desc.lower():
                setParamTooltips(tree)
                if resizeNameCol:
                    # Bug: Current 'resize to contents' makes the name column just a
                    # bit small
                    hint = tree.sizeHintForColumn(0)
                    tree.setColumnWidth(0, int(hint * 1.1))

        _param.sigTreeStateChanged.connect(maybeUpdateTips)

    if setTooltips:
        for param in treeParameters:
            hookupWrapper(param)
        setParamTooltips(tree)
    # hookupSignals(topParam)
    return tree


def setParametersExpanded(tree: ParameterTree, expandedVal=True):
    for item in tree.topLevelItems():
        for ii in range(item.childCount()):
            item.child(ii).setExpanded(expandedVal)
    tree.resizeColumnToContents(0)


def forceRichText(text: str):
    """
    Wraps text in <qt> tags to make Qt treat it as rich text. Since tooltips don't wrap
    nicely unless text is rich, this ensures all encountered tooltips are correctly
    wrapped.

    Parameters
    ----------
    text
        text, may already start with <qt> tags
    """
    if "PySide" in QT_LIB:
        richDetect = QtGui.Qt.mightBeRichText
    else:
        richDetect = QtCore.Qt.mightBeRichText
    if richDetect(text):
        return text
    return f"<qt>{text}</qt>"


def setParamTooltips(tree: ParameterTree, expandNameCol=False):
    iterator = QtWidgets.QTreeWidgetItemIterator(tree)
    item: QtWidgets.QTreeWidgetItem = iterator.value()
    while item is not None:
        # TODO: Set word wrap on long labels. Currently either can show '...' or
        #   wrap but not both
        # if tree.itemWidget(item, 0) is None:
        #   lbl = QtWidgets.QLabel(item.text(0))
        #   tree.setItemWidget(item, 0, lbl)
        if (
            hasattr(item, "parameter")
            and "tip" in item.param.opts
            and len(item.toolTip(0)) == 0
            and tree.itemWidget(item, 0) is None
        ):
            item.setToolTip(0, forceRichText(item.param.opts["tip"]))
        iterator += 1
        item = iterator.value()
    if expandNameCol:
        setParametersExpanded(tree, True)


def resolveYamlDict(cfgFname: FilePath, cfgDict: dict = None):
    if cfgDict is not None:
        cfg = cfgDict
    else:
        cfg = attemptFileLoad(cfgFname)
        if cfg is None:
            # Empty file
            cfg = {}
    if cfgFname is not None:
        cfgFname = Path(cfgFname)
    return cfgFname, cfg


def getParameterChild(
    param: Parameter,
    *childPath: t.Sequence[str],
    allowCreate=True,
    groupOpts: dict = None,
    childOpts: dict = None,
):
    if groupOpts is None:
        groupOpts = {}
    groupOpts.setdefault("type", "group")
    while childPath and childPath[0] in param.names:
        param = param.child(childPath[0])
        childPath = childPath[1:]
    # All future children must be created
    if allowCreate:
        for chName in childPath:
            param = param.addChild(dict(name=chName, **groupOpts))
            childPath = childPath[1:]
    elif len(childPath) > 0:
        # Child doesn't exist
        raise KeyError(f"Children {childPath} do not exist in parameter {param}")
    if childOpts is not None:
        if childOpts["name"] in param.names:
            param = param.child(childOpts["name"])
        else:
            param = param.addChild(childOpts)
    if not param.hasDefault():
        param.setDefault(param.value())
    return param


class ArgParseConverter(argparse.ArgumentParser):
    """
    Able to convert arguments to their types on parse_args
    """

    convertRemainder = True

    @staticmethod
    def argConverter(arg, returnSuccess=False):
        try:
            ret = ast.literal_eval(arg)
            success = True
        except:  # noqa
            # Many ways to fail a raw eval, catch by simply assuming a string type
            ret = arg
            success = False
        if returnSuccess:
            return ret, success
        return ret

    def _get_value(self, action, arg_string: str) -> t.Any:
        ret, success = self.argConverter(arg_string, returnSuccess=True)
        if not success:
            return super()._get_value(action, arg_string)
        return ret

    @classmethod
    def _lookAheadForValue(cls, extraIter, ii):
        try:
            nextK = extraIter[ii + 1]
            if nextK.startswith("--"):
                # This is also a flag condition, don't consume value this round
                vv = True
            else:
                vv = cls.argConverter(nextK)
                # Value consumed, move on an extra space
                ii += 1
        except IndexError:
            vv = True
        return vv, ii

    @classmethod
    def _consumeNextIterPos(cls, extraIter, ii):
        item = extraIter[ii]
        kk = vv = None
        if not item.startswith("--"):
            return kk, vv, ii + 1
        kk = item.strip("--")
        if "=" in kk:
            # Don't consume next key, this is the value
            kk, toParse = kk.split("=", 1)
            vv = cls.argConverter(toParse)
        else:
            vv, ii = cls._lookAheadForValue(extraIter, ii)
        return kk, vv, ii + 1

    def parse_args(self, args=None, namespace=None):
        namespace, args = super().parse_known_args(args, namespace)
        # Treat remainder as if they belonged
        named = vars(namespace)
        if not self.convertRemainder:
            return namespace
        extraIter = list(args)
        ii = 0
        while ii < len(extraIter):
            kk, vv, ii = self._consumeNextIterPos(extraIter, ii)
            if kk is not None:
                named[kk] = vv
        return Namespace(**named)


def makeCli(
    func: t.Callable, convertArgs=True, parserKwargs: dict = None, **procKwargs
):
    """
    Creates a CLI interface to a function from the provided function, parsing the
    documentation for help text, signature for default values, etc.

    Parameters
    ----------
    func
        Function from which to make a CLI interface
    convertArgs
        Whether to use a parser which converts string cli arguments to python values
    parserKwargs
        Passed to ArgumentParser on init
    **procKwargs
        Passed to AtomicProcess which is used as an intermediate to generate parameter
        documentation
    """
    from qtextras._funcparse import FROM_PREV_IO, QtExtrasInteractor

    def tipConverter(inStr):
        doc = QtGui.QTextDocument()
        doc.setHtml(inStr)
        return doc.toPlainText()

    funcDict = QtExtrasInteractor().functionToParameterDict(func, **procKwargs)
    tip = funcDict.get("tip", "")

    useCls = argparse.ArgumentParser if not convertArgs else ArgParseConverter
    parserKwargs = parserKwargs or {}
    parserKwargs.setdefault("description", tipConverter(tip))
    parser = useCls(**parserKwargs)

    for ch in funcDict["children"]:
        if "action" in ch["type"]:
            continue
        arg = parser.add_argument(
            f'--{ch["name"]}', required=ch["value"] is FROM_PREV_IO
        )
        if not arg.required:
            chType = type(ch["value"])
            if ch["value"] is not None:
                arg.type = chType
            arg.default = ch["value"]
        if "tip" in ch:
            arg.help = tipConverter(ch["tip"])
    return parser


def dialogGetSaveFileName(parent, winTitle, defaultTxt: str = None) -> t.Optional[str]:
    failedSave = True
    returnVal: t.Optional[str] = None
    while failedSave:
        saveName, ok = QtWidgets.QInputDialog().getText(
            parent,
            winTitle,
            winTitle + ":",
            QtWidgets.QLineEdit.Normal,
            str(defaultTxt),
        )
        # TODO: Make this more robust. At the moment just very basic sanitation
        for disallowedChar in ["/", "\\"]:
            saveName = saveName.replace(disallowedChar, "")
        if ok and not saveName:
            # User presses 'ok' without typing anything except disallowed characters
            # Keep asking for a name
            continue
        elif not ok:
            # User pressed 'cancel' -- Doesn't matter whether they entered a name or not
            # Stop asking for name
            break
        else:
            # User pressed 'ok' and entered a valid name
            return saveName
    return returnVal


def parameterDialog(parameter: Parameter, modal=True, show=None, exec=True):
    tree = flexibleParameterTree(parameter)
    setParametersExpanded(tree, True)
    dlg = QtWidgets.QDialog()
    layout = QtWidgets.QVBoxLayout()
    dlg.setLayout(layout)
    dlg.setModal(modal)
    layout.addWidget(tree)
    # Show before exec so size calculations are correct, and fix the height by a small
    # factor
    if show or (show is None and exec):
        dlg.show()
        dlg.resize(dlg.width(), dlg.height() + 25)
    if exec:
        dlg.exec_()
    return dlg


def hookupParamWidget(param: Parameter, widget):
    """
    Parameter widgets created outside parameter trees need to have their sigChanging,
    sigChanged, etc. signals hooked up to the parameter itself manually. The relevant
    code below was extracted from WidgetParameterItem
    """

    def widgetValueChanged():
        val = widget.value()
        return param.setValue(val)

    def paramValueChanged(param, val, force=False):
        if force or not pg.eq(val, widget.value()):
            try:
                widget.sigChanged.disconnect(widgetValueChanged)
                param.sigValueChanged.disconnect(paramValueChanged)
                widget.setValue(val)
                param.setValue(widget.value())
            finally:
                widget.sigChanged.connect(widgetValueChanged)
                param.sigValueChanged.connect(paramValueChanged)

    param.sigValueChanged.connect(paramValueChanged)
    if widget.sigChanged is not None:
        widget.sigChanged.connect(widgetValueChanged)

    if hasattr(widget, "sigChanging"):
        widget.sigChanging.connect(
            lambda: param.sigValueChanging.emit(param, widget.value())
        )

    # update value shown in widget.
    opts = param.opts
    if opts.get("value", None) is not None:
        paramValueChanged(param, opts["value"], force=True)
    else:
        # no starting value was given; use whatever the widget has
        widgetValueChanged()


def hierarchicalUpdate(
    baseDict: dict, newValuesDict: dict, replaceLists=True, uniqueListElements=False
):
    """
    Dictionary update that allows nested keys to be updated without deleting the
    non-updated keys
    """
    if not newValuesDict:
        return baseDict
    for k, v in newValuesDict.items():
        curVal = baseDict.get(k)
        if isinstance(curVal, dict) and isinstance(v, dict):
            hierarchicalUpdate(curVal, v, replaceLists, uniqueListElements)
        elif not replaceLists and isinstance(curVal, list) and isinstance(v, list):
            if uniqueListElements:
                v = [el for el in v if el not in curVal]
            curVal.extend(v)
        else:
            baseDict[k] = v
    return baseDict


def timedExec(
    updateFunc: t.Union[t.Generator, t.Callable],
    interval_ms: int,
    argLst: t.Sequence = None,
    stopCond: t.Callable[[], bool] = lambda: False,
):
    """
    Iterates over an argument list (or generator) and executes the next action every
    `interval_ms` ms. Useful for updating GUI elements periodically, e.g. showing a
    list of images one at a time. Set `interval_ms` to <= 0 to avoid starting right
    away.
    """
    timer = QtCore.QTimer()
    if argLst is None:
        # updateFunc must be a generator
        argLst = updateFunc()

        def updateFunc(_):
            return None

    argLst = iter(argLst)

    def update():
        if stopCond():
            timer.stop()
        try:
            arg = next(argLst)
            updateFunc(arg)
        except StopIteration:
            timer.stop()

    timer.timeout.connect(update)
    if interval_ms > 0:
        timer.start(interval_ms)
    return timer


def gracefulNext(generator: t.Generator):
    try:
        return next(generator)
    except StopIteration as ex:
        return ex.value


def naturalSorted(iterable):
    """
    Copied from tiffile implementation, but works with non-string objects (e.g. Paths)

    >>> naturalSorted(['f1', 'f2', 'f10'])
    ['f1', 'f2', 'f10']

    """

    def sortkey(x):
        x = str(x)
        return [(int(c) if c.isdigit() else c) for c in re.split(numbers, x)]

    numbers = re.compile(r"(\d+)")
    return sorted(iterable, key=sortkey)


class DummySignal:
    """
    Useful for spoofing a qt connection that doesn't do anything
    """

    def connect(self, *args):
        pass

    def disconnect(self, *args):
        pass

    def emit(self, *args):
        if self.capture:
            self.emissions.append(args)

    def __init__(self, capture=False):
        self.emissions = []
        self.capture = capture


@contextmanager
def makeDummySignal(signalHolder: QtCore.QObject, signalName: str, capture=False):
    oldSig = getattr(signalHolder, signalName)
    try:
        newSig = DummySignal(capture)
        setattr(signalHolder, signalName, newSig)
        yield newSig
    finally:
        setattr(signalHolder, signalName, oldSig)


@contextmanager
def overrideAttr(attrHolder, attrName: str, newVal):
    oldVal = getattr(attrHolder, attrName)
    try:
        setattr(attrHolder, attrName, newVal)
        yield
    finally:
        setattr(attrHolder, attrName, oldVal)


def getAnyPgColormap(name, forceExist=False):
    """
    Pyqtgraph allows file, matplotlib, or colorcet cmaps but doesn't allow getting from
    an arbitrary source. This simply shims access to ``pg.colormap.get`` which tries
    all sources each time a source-specific ``get`` fails.

    Parameters
    ----------
    name
        passed to ``pg.colormap.get``
    forceExist
        If *True*, the function will raise an error instead of returning *None* if the
        name was not found.
    """
    for source in None, "matplotlib", "colorcet":
        try:
            cmap = pg.colormap.get(name, source=source)
        except FileNotFoundError:
            # For None source when local file doesn't exist
            cmap = None
        if cmap is not None:
            return cmap
    # cmap = None at this point
    if forceExist:
        raise ValueError(
            f"'{name}' was not recognized among the available"
            f" options. Must be one of:\n{listAllPgColormaps()}"
        )
    # else
    return None


def listAllPgColormaps():
    """
    ``Shims pg.colormap.listMaps`` to list all colormaps (i.e. for all sources)
    """
    maps = []
    for source in None, "matplotlib", "colorcet":
        nextMaps = pg.colormap.listMaps(source)
        for curMap in nextMaps:
            if curMap not in maps:
                maps.append(curMap)
    return maps
