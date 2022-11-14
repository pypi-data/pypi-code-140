import b2luigi
import random


class MyNumberTask(b2luigi.Task):
    some_parameter = b2luigi.IntParameter()

    def output(self):
        return b2luigi.LocalTarget(f"results/output_file_{self.some_parameter}.txt")

    def run(self):
        random_number = random.random()
        with self.output().open("w") as f:
            f.write(f"{random_number}\n")


if __name__ == "__main__":
    b2luigi.set_setting("result_dir", "results")
    b2luigi.process([MyNumberTask(some_parameter=i) for i in range(100)],
                    workers=200)
