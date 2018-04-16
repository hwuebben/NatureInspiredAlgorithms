class ProblemDefinition:
    """
    store the problem definition in a static manner so all modules can access it
    """
    #static variable to store the number of machines
    nrMachines = None
    #static variable to store the runtimes per job
    jobRuntimes = None
    #static variable to store the number of jobs
    nrJobs = None

    @staticmethod
    def setPD(nrMachines,jobRuntimes):
        """
        set the Problem Instance
        :param nrMachines:
        :param nrJobs:
        :param jobRuntimes:
        :return:
        """
        ProblemDefinition.nrMachines = nrMachines
        ProblemDefinition.nrJobs = jobRuntimes.size
        ProblemDefinition.jobRuntimes = jobRuntimes
