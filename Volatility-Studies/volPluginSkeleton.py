#import list

class CmdLine(interfaces.plugin.PluginInterface):#creation of inheritable class
    @classmethod
    def get_requirements(cls):#Requirements
        pass
    def run(self):#Define Run
        pass
    def generator(self, procs): #define generator (secondary function to run to speed up process)
        pass