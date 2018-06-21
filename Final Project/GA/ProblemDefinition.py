class ProblemDefinition:

    def __init__(self, nrMachines, jobRuntimes):
        """
        Set the Problem Instance
        :param nrMachines: Number of machines
        :param jobRuntimes: Runtimes per job
        :return:
        """

        self.nrMachines = nrMachines
        self.nrJobs = jobRuntimes.size  # Number of jobs
        self.jobRuntimes = jobRuntimes
