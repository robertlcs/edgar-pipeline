from subprocess import call, Popen, PIPE, STDOUT

def execute_command(cmd):
    print "Executing command: %s" % cmd
    ps = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    (output, err_output) = ps.communicate()
    print output
    print err_output
    return output, err_output
