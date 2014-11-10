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
        pass

if __name__ == "__main__":
    unittest.main()
