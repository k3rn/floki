import unittest
from floki.machines import Machines


class functions_with_return(unittest.TestCase):

    def setUp(self):
        self.config = 0
        self.machine = Machines('config.yml')

    def test_get_vmx_path(self):
        self.assertEqual(self.machine.get_vmx_path('development',
                                                   'main-servers',
                                                   'web01'),
                         '/Volumes/Hulk/VirtualMachines/skaro/development/' +
                         'web01.vmwarevm/web01.vmx')

    def test_get_vmx_path_with_path_set(self):
        self.assertEqual(self.machine.get_vmx_path('development',
                                                   'main-servers',
                                                   'web04'),
                         '/Volumes/Hulk/VirtualMachines/templates/' +
                         'debian-amd64.vmwarevm/debian-amd64.vmx')

    def test_get_list(self):
        result = {'cache01': '/Volumes/Hulk/VirtualMachines/skaro/' +
                             'development/cache01.vmwarevm/cache01.vmx',
                  'cache02': '/Volumes/Hulk/VirtualMachines/skaro/' +
                             'development/cache02.vmwarevm/cache02.vmx'}
        self.assertEqual(self.machine.get_list('development', ['alt-servers']),
                         result)

    def test_get_list_with_all_groups(self):
        groups = ['all']
        result = {'cache01': '/Volumes/Hulk/VirtualMachines/skaro/' +
                             'development/cache01.vmwarevm/cache01.vmx',
                  'cache02': '/Volumes/Hulk/VirtualMachines/skaro/' +
                             'development/cache02.vmwarevm/cache02.vmx',
                  'web04': '/Volumes/Hulk/VirtualMachines/templates/' +
                           'debian-amd64.vmwarevm/debian-amd64.vmx',
                  'web03': '/Volumes/Hulk/VirtualMachines/skaro/' +
                           'development/web03.vmwarevm/web03.vmx',
                  'web01': '/Volumes/Hulk/VirtualMachines/skaro/' +
                           'development/web01.vmwarevm/web01.vmx',
                  'db02': '/Volumes/Hulk/VirtualMachines/skaro/' +
                          'development/db02.vmwarevm/db02.vmx',
                  'db01': '/Volumes/Hulk/VirtualMachines/skaro/' +
                          'development/db01.vmwarevm/db01.vmx'}
        self.assertEqual(self.machine.get_list('development', groups), result)

    def test_get_list_running_norunning(self):
        self.assertEqual(len(self.machine.get_list_running({'count': 0},
                                                           'development',
                                                           ['all'])),
                         0)

    def test_get_list_running(self):
        machinerunning = "".join('/Volumes/Hulk/VirtualMachines/skaro/' +
                                 'development/db01.vmwarevm/db01.vmx')

        running = {'count': 1,
                   'machines': [machinerunning,
                                '/Volumes/Hulk/VirtualMachines/notinthelist']}
        self.assertEqual(self.machine.get_list_running(running,
                                                       'development',
                                                       ['all']
                                                       ),
                         {'db01': machinerunning})

if __name__ == "__main__":
    unittest.main()
