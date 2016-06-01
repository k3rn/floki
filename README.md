Floki: Orchestrate VMware Fusion virtual machines.
==================================================

The configuration is done through a YAML file, the default is `floki.yml` on
the current directory.

You can see below an example of an configuration file.
```yaml
---
- project:
    name: skaro
    dir: /Volumes/Hulk/VirtualMachines
    template: /Volumes/Hulk/VirtualMachines/templates/debian.vmwarevm
- machines:
        development: &default
           	webserver:
                web01:
                web02:
            application:
                app01:
					cpu: 2
					memory: 2048
				app02:
			database:
				db01:
		staging: &development
```

The `- project` section set the options for project.

	- "name: " define the name of the project
	- "dir: " define where the directory with the project name that stores the
	  virtual machines will be.
	- "template: " defines which virtual machine will be used as a template to
	  create the virtual machines for this project.

The `- machines` list the groups and its machines.

	- The fist level lists the enviroment, in the example the enviroments are
	  "development" and "staging".
	- The second level lists the groups of machines, in the example they are
	  "webserver", "application", "database".
	- The third level lists the machines in the groups.
	- The fourth level sets the how much memory (in MB) and the number of cpus
	  a virtual machines. If this options are not set, they are going to be the
	  same as the template.
