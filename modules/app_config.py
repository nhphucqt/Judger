import os
from modules.functions import *

# -i, --ignore-case               ignore case differences in file contents
# -E, --ignore-tab-expansion      ignore changes due to tab expansion
# -Z, --ignore-trailing-space     ignore white space at line end
# -b, --ignore-space-change       ignore changes in the amount of white space
# -w, --ignore-all-space          ignore all white space
# -B, --ignore-blank-lines        ignore changes where lines are all blank
# -I, --ignore-matching-lines=RE  ignore changes where all lines match RE

diff_options = {
    "binary" : "",
    "normal" : "--ignore-trailing-space --ignore-blank-lines",
    "case"   : "--ignore-case --ignore-trailing-space --ignore-blank-lines",
    "checker": "custom check option (same as Themis)"
}

build_command = {
    "cmd": "g++",
    "arg": [
        "-std=c++14",
        "-Wall",
        "-O2"
    ]
}

cwd = os.getcwd() + "/"

temp_dir = cwd + "tmp/"
resources_dir = cwd + "resources/"
scripts_dir = cwd + "scripts/"

checker_messages = temp_dir + "checker_messages"
checker_input = temp_dir + "checker_input"

last_commands_path = resources_dir + "last_commands"
status_path = resources_dir + "status"

timeout_path = scripts_dir + "timeout"

tasks_path = cwd + "tasks/" # must be absolute path
codes_path = cwd + "codes/" # must be absolute path

history_path = codes_path + "history/"

last_comds = []

create_dir(temp_dir)
create_dir(tasks_path)
create_dir(codes_path)
create_dir(history_path)
create_dir(resources_dir)