import vmfusion
import yaml
import sys


class Machines:

    def __init__(self, config):
        self.load_config(config)
        self.vmrun = vmfusion.vmrun_cli()

    def load_config(self, path):
        try:
            self.config = yaml.load(file(path, 'r'))
        except IOError, e:
            print str(e)

    def get_vmx_path(self, env, group, name):
        machine = self.config[1]['machines'][env][group][name]

        if type(machine) is dict and 'path' in machine:
            path = machine['path']
        else:
            path = "".join(self.config[0]['project']['dir'] + '/' +
                           self.config[0]['project']['name'] + '/' + env +
                           '/' + name + '.vmwarevm/' + name + '.vmx')

        return path

    def get_list(self, env, groups):

        list = dict()
        if groups[0] is 'all':
            groups = self.config[1]['machines'][env].keys()

        for group in groups:
            try:
                for name in self.config[1]['machines'][env][group]:
                    list[name] = self.get_vmx_path(env, group,  name)

            except KeyError:
                if env not in self.config[1]['machines']:
                    print "ERROR: Enviroment %s doesn't exist" % env
                else:
                    print "ERROR: Group %s doesn't exist" % group

        if any(list):
            return list
        else:
            sys.exit(1)

    def get_list_running(self, env, groups):
        running_list = dict()
        for running in self.vmrun.list()['machines']:
            for name in self.get_list(env, groups):
                if running == self.get_list(env, groups)[name]:
                    running_list[name] = running

        return running_list

    def start(self, env, groups):
        machinelist = self.get_list(env, group)
        for machine in machinelist:
            try:
                print "Starting %s:" % machine,
                self.vmrun.start(machinelist[machine], False)
                print "ok"
            except ValueError, e:
                print "ERROR: %s" % str(e)

    def stop(self, env, groups):
        for machine in self.get_list_running(env, groups):
            try:
                print "Stopping %s" % machine,
                self.vmrun.stop(get_vmx_path(env, group, machine), False)
                print "ok."
            finally:
                print "failed."

    def restart(self, name, path):
        pass

    def suspend(self, name, path):
        pass

    def status(self, env, group):
        running_list = self.get_list_running(env, group)
        print "Machines running:"
        for machine in running_list:
            print machine
        print "Total: %s machine(s) running" % len(running_list)
        print group

    def create(self, env):
        pass
