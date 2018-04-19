import numpy as np

class Benchmark:
    def benchmark1():
        jobRuntimes = np.append(np.random.randint(10, 1001, 200), np.random.randint(100, 301, 100))
        return [20, jobRuntimes]

    def benchmark2():
        jobRuntimes = np.append(np.random.randint(10, 1001, 150), np.random.randint(400, 701, 150))
        return [20, jobRuntimes]

    def benchmark3():
        jobRuntimes = [50]
        for i in range(100):
            jobRuntimes.append(i // 2 + 50)
        return [50, np.asarray(jobRuntimes)]
