from vmrun_wrapper.vmrun import machine
import yaml
import sys
import os
import time


class Machines:

    def __init__(self, config):
        self.load_config(config)
        if os.environ.get('VMRUN'):
            self.vm = machine.machine(os.environ['VMRUN'])
        else:
            self.vm = machine.machine()

    def load_config(self, path):
        try:
            self.config = yaml.load(file(path, 'r'))
        except IOError, e:
            print str(e)

    def get_vmx_path(self, env, group, name):
        machines = self.config[1]['machines'][env]
        if group is not None:
            machine = machines[group][name]
        else:
            for group in machines:
                if name in machines[group]:
                    machine = machines[group][name]

        if type(machine) is dict and 'path' in machine:
            path = machine['path']
        else:
            path = "".join(self.config[0]['project']['dir'] + '/' +
                           self.config[0]['project']['name'] + '/' + env +
                           '/' + name + '.vmwarevm')

        return path

    def does_machine_exists(self, machine_path):
        if os.path.isdir(machine_path) and machine_path.endswith('vmwarevm'):
            for file in os.listdir(machine_path):
                if file.endswith('.vmx'):
                    if os.path.isfile(machine_path + '/' + file):
                        return True
        elif machine_path.endswith('vmx') and os.path.isfile(machine_path):
            if os.path.isfile(machine_path):
                return True
        else:
            return False

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
        machine_list = self.get_list(env, groups)
        if running['count'] is not 0:
            for machine in machine_list:
                for path in running['machines']:
                    if machine_list[machine] in path:
                        running_list[machine] = path
        return running_list

    def generate_inventory(self, env, groups):
        """
        Generate a inventory file to be used with Ansible

        """
        if groups[0] is 'all':
            groups = self.config[1]['machines'][env].keys()

        metavar = dict()
        inventory = dict()

        try:
            for group in groups:
                machines = self.config[1]['machines'][env][group]
                inventory[group] = list()
                for name in machines:
                    inventory[group].append(name)
                    ip = self.vm.get_ip(self.get_vmx_path(env, group,
                                                          name))
                    if ip == '\n':
                        for i in range(0, 5):
                            time.sleep(5)
                            ip = self.vm.get_ip(self.get_vmx_path(env, group,
                                                                  name))
                            if ip != '\n':
                                break

                    if 'Error' not in ip:
                        metavar[name] = {"ansible_host": ip.rstrip()}
                    else:
                        raise ValueError
        except:
            print "failed."

        inventory.update({"_meta": {"hostvars": metavar}})
        return inventory

    def start(self, env, groups, single):
        machine_list = self.get_list(env, groups)
        if single is None:
            for machine in machine_list:
                try:
                    print "[%s] Starting %s:" % (env, machine),
                    if self.does_machine_exists(machine_list[machine]):
                        self.vm.start(machine_list[machine], False)
                        print "ok"
                except IOError, e:
                    print " %s" % str(e)
        else:
            try:
                self.vm.start(machine_list[single], False)
            except KeyError:
                print "The machine %s is not in the inventory." % single

    def stop(self, env, groups, single):
        machines_running = self.get_list_running(self.vm.list(), env, groups)
        if single is None:
            for machine in machines_running:
                try:
                    print "[%s] Stopping %s:" % (env, machine),
                    self.vm.stop(machines_running[machine], False)
                    print "ok."
                except:
                    print "failed."
        else:
            print "Stoping %s: " % single,
            try:
                self.vm.stop(machines_running[single], False)
                print "ok."
            except KeyError:
                print "failed. Machine is not running."

    def restart(self, env, groups):
        stop(env, groups)
        start(env, groups)

    def suspend(self, env, groups):
        for machine in self.get_list_running(self.vm.list(), env, groups):
            try:
                print "[%s] Suspending %s" % (env, machine),
                self.vm.stop(get_vmx_path(env, group, machine), False)
                print "ok."
            finally:
                print "failed."

    def status(self, env, group, single):
        running_list = self.get_list_running(self.vm.list(), env, group)
        if single is None:
            if len(running_list) is 0:
                print 'No machine running'
            else:
                print "Machines running:"
                for machine in running_list:
                    print machine
                print "Total: %s machine(s) running" % len(running_list)
        elif single in running_list:
            print "The machine %s is running." % single
        else:
            print "The machine %s is not running." % single

    def create(self, env, groups, single):
        machine_list = self.get_list(env, groups)
        if single is not None and single in machine_list:
            machine_list = {single: self.get_vmx_path(env, None, single)}
        template = self.config[0]['project']['template']

        if not self.does_machine_exists(template):
            print "The template %s doesn\'t exist." % template

        for machine in machine_list:
            if self.does_machine_exists(machine_list[machine]) and False:
                print "%s" % machine_list[machine],
                print "Already exists, not creating."
            else:
                print "[%s] Creating %s..." % (env, machine),
                try:
                    os.makedirs(machine_list[machine])
                except OSError:
                    if not os.path.isdir(machine_list[machine]):
                        raise
                vmx_dest_path = machine_list[machine] + '/' + machine + '.vmx'
                if not os.path.isfile(vmx_dest_path):
                    self.vm.clone(template, vmx_dest_path)
                    print "done."
                else:
                    print "skiping, virtual machine already exists."
