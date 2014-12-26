from vmrun_wrapper.vmrun import machine
import yaml
import sys
import os


class Machines:

    def __init__(self, config):
        self.load_config(config)
        self.vm = machine.machine()

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
                           '/' + name + '.vmwarevm')

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

    def get_list_running(self, running, env, groups):
        running_list = dict()
        if running['count'] is not 0:
            for running in running['machines']:
                for name in self.get_list(env, groups):
                    if running == self.get_list(env, groups)[name]:
                        running_list[name] = running

        return running_list

    def start(self, env, groups):
        machines_running = self.get_list_running(self.vm.list(), env, groups)
        machine_list = self.get_list(env, groups)
        for machine in machine_list:
            try:
                if machines_running.keys().count(machine) is 0:
                    print "Machine %s is already running." % machine
                else:
                    print "Starting %s:" % machine,
                    self.vm.start(machine_list[machine], False)
                    print "ok"
            except ValueError, e:
                print "ERROR: %s" % str(e)

    def stop(self, env, groups):
        machine_list = self.get_list_running(self.vm.list(), env, groups)
        for machine in machine_list:
            try:
                print "Stopping %s" % machine,
                self.vmrun.stop(get_vmx_path(env, group, machine), False)
                print "ok."
            finally:
                print "failed."

    def restart(self, env, groups):
        stop(env, groups)
        start(env, groups)

    def suspend(self, env, groups):
        for machine in self.get_list_running(self.vm.list(), env, groups):
            try:
                print "Suspending %s" % machine,
                self.vm.stop(get_vmx_path(env, group, machine), False)
                print "ok."
            finally:
                print "failed."

    def status(self, env, group):
        running_list = self.get_list_running(self.vm.list(), env, group)
        if len(running_list) is 0:
            print 'No machine running'
        else:
            print "Machines running:"
            for machine in running_list:
                print machine
            print "Total: %s machine(s) running" % len(running_list)

    def create(self, env):
        pass
