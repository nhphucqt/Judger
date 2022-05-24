import datetime
import os
import shutil
import stat
import subprocess
import sys

from modules import hyperlink
from modules import textcolor
from modules.app_config import *

commands = {
    "help": {
        "cmd": "help | help [command]", 
        "desc": "Print available commands and command description",
        "argc": [0, 1],
        "run": lambda comd: help(comd)
    },
    "jd": {
        "cmd": "jd [name]",
        "desc": "Judge [name]",
        "argc": [1],
        "run": lambda comd: judge(comd[1])
    },
    "submit": {
        "cmd": "submit [name]",
        "desc": "Submit code [name]",
        "argc": [1],
        "run": lambda comd: submit(comd[1])
    },
    "lst": {
        "cmd": "lst",
        "desc": "List tasks",
        "argc": [0],
        "run": lambda comd: list_tasks()
    },
    "lsc": {
        "cmd": "lsc",
        "desc": "List available codes",
        "argc": [0],
        "run": lambda comd: list_codes()
    },
    "path": {
        "cmd": "path",
        "desc": "Print tasks' path and codes's path",
        "argc": [0],
        "run": lambda comd: print_path()
    },
    "show": {
        "cmd": "show [name]",
        "desc": "Show task [name]",
        "argc": [1],
        "run": lambda comd: list_testcases(comd[1])
    },
    "view": {
        "cmd": "view [name]",
        "desc": "View code [name]",
        "argc": [1],
        "run": lambda comd: view_code(comd[1])
    },
    "history": {
        "cmd": "history [name]",
        "desc": "View all last submissions of task [name]",
        "argc": [1],
        "run": lambda comd: list_history(comd[1])
    },
    "exit": {
        "cmd": "exit",
        "desc": "Exit this program",
        "argc": [0],
        "run": lambda comd: sys.exit(0)
    },
    "l": {
        "cmd": "l",
        "desc": "Run last command",
        "argc": [0],
        "run": lambda comd: run_last_command()
    },
    "c": {
        "cmd": "c",
        "desc": "Show options of last 9 commands",
        "argc": [0],
        "run": lambda comd: choose_last_commands()
    }
}

def get_task_path(task_name):
    return tasks_path + task_name + "/"

def get_code_path(code_name):
    return codes_path + code_name + ".cpp"

def is_exist_task(task_name):
    return os.path.isdir(get_task_path(task_name))

def is_exist_code(code_name):
    return os.path.isfile(get_code_path(code_name))

def help(comd):
    print()
    if len(comd) == 1:
        for cmd in sorted(commands):
            print("•", cmd)
    else:
        if not comd[1] in commands:
            print("This command doesn't exist!")
            return
        print("Command:", commands[comd[1]]["cmd"])
        print("Description:", commands[comd[1]]["desc"])

def list_tasks():
    tasks_list = os.listdir(tasks_path)
    tasks_list = list(filter(lambda task: os.path.isdir(tasks_path+task), tasks_list))
    tasks_list.sort(key=lambda e: e.lower())

    maxLen = 0
    if len(tasks_list) > 0:
        maxLen = max(map(lambda task: len(task), tasks_list))
    maxIdLen = len(str(len(tasks_list)))

    print()
    for id,task in zip(range(len(tasks_list)),tasks_list):
        test_path = tasks_path + task + "/"
        with open(test_path+"config") as fi:
            test_config = fi.read().split('\n')
        print(f"#{str(id).ljust(maxIdLen)} | {textcolor.bold(task.ljust(maxLen))} | {test_config[0]}s {test_config[1]}kB {test_config[2]}")
    print()
    print(f"Total {len(tasks_list)} tasks")

def list_codes():
    codes_list = os.listdir(codes_path)
    codes_list = list(filter(lambda code: os.path.isfile(codes_path+code), codes_list))
    codes_list.sort(key=lambda e: e.lower())

    maxIdLen = len(str(len(codes_list)))

    print()
    for id,code in zip(range(len(codes_list)), codes_list):
        print(f"#{str(id).ljust(maxIdLen)} | {textcolor.bold(code)}")

    print()
    print(f"Total {len(codes_list)} codes")

def list_testcases(task_name):
    test_path = tasks_path + task_name + "/"
    if not os.path.isdir(test_path):
        print("Test path doesn't exist")
        return
    
    testcases_list = os.listdir(test_path)
    testcases_list = list(filter(lambda testcase : os.path.isdir(test_path+testcase), testcases_list))
    testcases_list.sort()

    with open(test_path+"config") as fi:
        test_config = fi.read().split('\n')
    test_config = list(map(lambda x: x.strip(), test_config))

    print()
    print(textcolor.fore(f"Time   : {test_config[0]}s", 247))
    print(textcolor.fore(f"Memory : {test_config[1]}kB", 247))
    print(textcolor.fore(f"Check  : {test_config[2]}", 247))
    print()

    for testcase, test_idx in zip(testcases_list, range(len(testcases_list))):
        print(textcolor.bold(textcolor.fore(f"#{str(test_idx).ljust(len(str(len(testcases_list)))+1)}:", 245)), end=' ')
        print(textcolor.light(hyperlink.link(f"file://{test_path}{testcase}/", f"{task_name}/{testcase}")))

def list_history(task_name):
    print()
    history_task_path = history_path + task_name + "/"
    if not os.path.isdir(history_task_path):
        print("Test path doesn't exist")
        return
    
    history_list = os.listdir(history_task_path)
    history_list = list(filter(lambda code : os.path.isfile(history_task_path+code), history_list))
    history_list.sort()

    for code, code_idx in zip(history_list, range(len(history_list))):
        print(textcolor.bold(textcolor.fore(f"#{str(code_idx).ljust(len(str(len(history_list)))+1)}:", 245)), end=' ')
        print(textcolor.light(hyperlink.link(f"file://{history_task_path}{code}/", code)))

def print_path():
    print("Tasks:","file://"+tasks_path)
    print("Contestant:","file://"+codes_path)

def view_code(code_name):
    if not is_exist_code(code_name):
        print("Code path doesn't exist")
    os.system(f"view {get_code_path(code_name)}")

def judge(task_name):
    if not is_exist_task(task_name):
        print("Test path doesn't exist")
        return
    if not is_exist_code(task_name):
        print("Code path doesn't exist")
        return

    test_path = get_task_path(task_name)
    code_path = get_code_path(task_name)

    with open(test_path+"config") as fi:
        test_config = fi.read().split('\n')
    test_config = list(map(lambda x: x.strip(), test_config))

    print()
    print(textcolor.bold("Time   : " + test_config[0] + "s"))
    print(textcolor.bold("Memory : " + test_config[1] + "kB"))
    print(textcolor.bold("Check  : " + test_config[2]))
    print()

    rename_dir_elements(test_path)

    print(textcolor.trans("Compiling code...\n", fr=45, st="b"))
    build_comd = f"{build_command['cmd']} {' '.join(build_command['arg'])} \'{code_path}\' -o \'{temp_dir}{task_name}\'"
    print(textcolor.bold("Command:"), build_comd)
    print()
    if not os.system(build_comd):
        print(textcolor.trans("\nCompiled sucessfully\n", fr=48, st="b"))
    else: 
        return
    
    exec_file = temp_dir + task_name

    testcases_list = os.listdir(test_path)
    testcases_list = list(filter(lambda testcase : os.path.isdir(test_path+testcase), testcases_list))
    testcases_list.sort()

    status_color = { "ac": 46, "pa": 11, "wa": 196, "rte": 208, "tle": 241, "mle": 202 }
    result = { "ac": 0, "pa": 0, "wa": 0, "rte": 0, "tle": 0, "mle": 0 }

    for testcase, test_idx in zip(testcases_list, range(len(testcases_list))):
        testcase_path = test_path + testcase + "/"
        testcase_input_path = testcase_path + task_name + ".inp"
        testcase_output_path = temp_dir + task_name + ".out"

        print(textcolor.bold(hyperlink.link("file://"+testcase_path, f"Testcase #{str(test_idx).ljust(len(str(len(testcases_list))))}:")), end=' ')
        
        run_code = f"\'{exec_file}\' < \'{testcase_input_path}\' > \'{testcase_output_path}\' 2> /dev/null"
        run_command = f"{timeout_path} -t {test_config[0]} -m {test_config[1]} \"{run_code}\" 2> {status_path}"
        exit_code = subprocess.run(run_command, shell=True).returncode

        with open(status_path) as fi:
            status = fi.readline().split()
            
        if exit_code != 0:
            result["rte"] += 1
            print(textcolor.trans("RTE", fr=status_color["rte"], st="b"), end=' ')
            print(f"[{status[2]}s]")
        else:
            if status[0] == "TIMEOUT":
                result["tle"] += 1
                print(textcolor.trans("TLE", fr=status_color["tle"], st="b"), end=' ')
                print(f"[{float(test_config[0]):.2f}s]")
            elif status[0] == "MEM":
                result["mle"] += 1
                print(textcolor.trans("MLE", fr=status_color["mle"], st="b"), end=' ')
                print(f"[{status[2]}s]")
            elif status[0] == "FINISHED":
                # 0 : Accepted
                # 1 : Wrong Answer
                # 2 : diff trouble
                # 3 : Partial Accepted
                check = 0
                if test_config[2] == "checker":
                    with open(checker_input, 'w') as fo:
                        fo.writelines([testcase_path, '\n', temp_dir])
                    subprocess.run(f"{test_path}Check{task_name} < {checker_input} > {checker_messages}", shell=True)
                    with open(checker_messages) as messages:
                        message_lines = messages.read().split('\n')
                        message_lines = list(filter(lambda x: x != '', message_lines))
                        score = message_lines[-1]
                        score = float(score)
                        assert(score >= 0.0 and score <= 1.0)
                        if score == 1.0: check = 0
                        elif score == 0.0: check = 1
                        else: check = 3
                else:
                    testcase_answer_path = testcase_path + task_name + ".out"
                    check = subprocess.run(f"diff {diff_options[test_config[2]]} {testcase_answer_path} {testcase_output_path} > /dev/null", shell=True).returncode
                if check == 0:
                    result["ac"] += 1
                    print(textcolor.trans("AC", fr=status_color["ac"], st="b"), end='  ')
                elif check == 1:
                    result["wa"] += 1
                    print(textcolor.trans("WA", fr=status_color["wa"], st="b"), end='  ')
                elif check == 3:
                    result["pa"] += 1
                    print(textcolor.trans("PA", fr=status_color["pa"], st="b"), end='  ')
                elif check == 2:
                    assert(False)
                else:
                    assert(False)
                print(f"[{status[2]}s]")
                if test_config[2] == "checker":
                    with open(checker_messages) as messages:
                        message_lines = messages.read().split('\n')
                        for line in message_lines:
                            print(textcolor.fore(">>", 3), line) 
            else:
                print("Unknown status")
    print()
    print("•",textcolor.bold(task_name),"•")
    print()
    print(f"Passed {result['ac']}/{len(testcases_list)} testcases")
    print()
    print(f"- {textcolor.trans('AC', fr=status_color['ac'], st='b')}  :", result["ac"])
    print(f"- {textcolor.trans('PA', fr=status_color['pa'], st='b')}  :", result["pa"])
    print(f"- {textcolor.trans('WA', fr=status_color['wa'], st='b')}  :", result["wa"])
    print(f"- {textcolor.trans('RTE', fr=status_color['rte'], st='b')} :", result["rte"])
    print(f"- {textcolor.trans('TLE', fr=status_color['tle'], st='b')} :", result["tle"])
    print(f"- {textcolor.trans('MLE', fr=status_color['mle'], st='b')} :", result["mle"])

def history_encode(task_name):
    return task_name + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f") + ".cpp"

def submit(task_name):
    if not is_exist_task(task_name):
        print("Task path doesn't exist")
        return
	
    code_path = get_code_path(task_name)
    tmp_code_path = temp_dir + task_name + "_submission"
    with open(tmp_code_path, "w") as fo: # Create and clear file
        pass
    # Open gedit to paste code
    os.system(f"gedit -w {tmp_code_path}") 
    with open(tmp_code_path) as fi:
        if fi.read() == "":
            os.remove(tmp_code_path)
            print("Cancel submission")
            return

    history_task_path = history_path + task_name + "/"
    history_code_path = history_task_path + history_encode(task_name)
    create_dir(history_task_path)
    shutil.copy(tmp_code_path, history_code_path)
    os.chmod(history_code_path, stat.S_IREAD)
    shutil.move(tmp_code_path, code_path)
    judge(task_name)

def push_comds(comd):
    comd = " ".join(comd)
    if len(last_comds) == 0 or last_comds[-1] != comd:
        last_comds.append(comd)
        with open(last_commands_path, "a") as fo:
            fo.writelines(comd+'\n')

def run_last_command():
    if len(last_comds) == 0:
        print("No recent commands")
    else:
        print("Running", last_comds[-1])
        app_run(last_comds[-1].split(), True)
    raise Exception("")

def choose_last_commands():
    comds = last_comds[-9:]
    print()
    print(textcolor.fore("0 -> cancel", 11))
    for i, c in zip(range(len(comds)), comds):
        print(f"{i+1} -> {c}")
    print()
    while True:
        id = input("Enter id: ")
        try: 
            id = int(id) - 1
            if id == -1:
                break
            if id in range(len(comds)):
                print("Running", comds[id])
                app_run(comds[id].split(), True)
                break
            print(f"id = {id} is not in range [0, {len(comds)}]")
        except ValueError:
            print(f"id = {id} is not a number")
    raise Exception("")

def app_run(comd, save):
    # print(">>", comd, "|", save)
    if len(comd) == 0 or not comd[0] in commands:
        raise Exception("Invalid command")
    expected_argc(comd, commands[comd[0]]["argc"])
    commands[comd[0]]["run"](comd)
    if save:
        push_comds(comd)

if __name__ == "__main__":
    if os.path.isfile(last_commands_path):
        with open(last_commands_path) as fi:
            last_comds = fi.read().split('\n')
    else:
        last_comds = ['']
    with open(last_commands_path, "w") as fo:
        fo.write('\n'.join(last_comds[-1001:]))
    last_comds = list(filter(lambda comd: comd != "", last_comds))

    while True:
        try:
            app_run(input("Enter command: ").split(), True)
        except Exception as exc:
            if str(exc) != "":
                print(exc)
        print()
        print(textcolor.trans('•', fr=196, st="b"), end="")
        print(textcolor.trans('•', fr=226, st="b"), end="")
        print(textcolor.trans('•', fr=40, st="b"))
        print()