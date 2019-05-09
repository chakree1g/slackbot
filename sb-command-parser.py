import shlex

def slackbot_command_parse(input_line_of_text,begins_with='/slackbot'):
    """ Evaluate an input line of text, extract and return a data structure for a slackbot command.
    Expected syntax for slackbot commands:
      /slackbot create <task_name>:<task_description (in quotes)>:<priority_level>:<percent_completion>
      /slackbot update <task_name>:{optional <task_description>}:{optional <priority_level>}:<percent_completion>
      /slackbot suspend  <task_name>
      /slackbot abandon  <task_name>
    Returned data structure: dictionary, with 5 keys:
       'Command','Task Name','Task Description','Priority Level','Percent Completion'
    Values for keys ('Command','Task Name','Task Description') are strings
    Values for keys ('Priority Level','Percent Completion') are integers or empty strings.
    Basic command parameter value verification is performed.
    :param input_line_of_text: input line of text.
    :param begins_with: string that the command is supposed to start with.
    """

    # declare returned data structure
    ret_dict = {}

    # some local variables
    priority_level_list = [0,1,2]
    # column names
    col_command = 'Command'
    col_taskname = 'Task Name'
    col_taskdesc = 'Task Description'
    col_priolevel = 'Priority Level'
    col_percent = 'Percent Completion'

    try:

        # use shlex: Shell-like lexical analysis
        parsed_input = shlex.split(input_line_of_text)
        # if the input is a slackbot command, then we should have:
        # parsed_input[0] == '/slackbot'           : keyword for slackbot
        # parsed_input[1] == <command>             : keywork for the slackbot command
        # parsed_input[2] == <tn:{td}:{pl}:{pc}>   : parameters of slackbot command

        # check that the first token is '/slackbot' (slash, 'slackbot'), or the user argument begins_with
        if parsed_input[0] == begins_with:

            # following blocks: specific processing for each slackbot command

            # specific processing for: create
            COMMAND = 'create'
            if parsed_input[1] == COMMAND:
                param_list = parsed_input[2].split(':')
                # length must be exactly 4, and all parameters must be correct
                #   (TN task_name, TD task_description, PL priority_level, PC percent_completion)
                # need to cast PL and PC as int (because they are strings)
                # note: range (a,b) goes from a to b-1 : [a;b-1], or [a;b[ (if a and b are integers, and a<b)
                if len(param_list) == 4:
                    # basic parameter value checks
                    if ( (len(param_list[0]) > 0) and (len(param_list[1]) > 0) and
                         (int(param_list[2]) in priority_level_list) and (int(param_list[3]) in range(0,101)) ):
                        ret_dict = {col_command:COMMAND,
                                    col_taskname:param_list[0],
                                    col_taskdesc:param_list[1],
                                    col_priolevel:int(param_list[2]),
                                    col_percent:int(param_list[3])}

            # specific processing for: update
            COMMAND = 'update'
            if parsed_input[1] == COMMAND:
                param_list = parsed_input[2].split(':')
                # length must be exactly 4, but TD and PL can be empty
                if len(param_list) == 4:
                    # basic parameter value checks: only TN and PC; TD can be added even if empty, no need to check
                    if (len(param_list[0]) > 0) and (int(param_list[3]) in range(0, 101)):
                        # check for optional PL; but don't create return value if incorrect
                        # (if PL is there, it has to be valid)
                        if len(param_list[2])>0:
                            if int(param_list[2]) in priority_level_list:
                                ret_dict = {col_command: COMMAND,
                                            col_taskname: param_list[0],
                                            col_taskdesc: param_list[1],
                                            col_priolevel: int(param_list[2]),
                                            col_percent: int(param_list[3])}
                            # else, do not return the dictionary: priority level was invalid
                        else:
                            ret_dict = {col_command: COMMAND,
                                        col_taskname: param_list[0],
                                        col_taskdesc: param_list[1],
                                        col_priolevel: '',
                                        col_percent: int(param_list[3])}

            # specific processing for: suspend
            COMMAND = 'suspend'
            if parsed_input[1] == COMMAND:
                param_list = parsed_input[2].split(':')
                # length should be exactly 1
                if len(param_list) == 1:
                    # basic parameter value checks: only TN
                    if len(param_list[0]) > 0:
                        ret_dict = {col_command: COMMAND,
                                    col_taskname: param_list[0],
                                    col_taskdesc: '',
                                    col_priolevel: '',
                                    col_percent: ''}

            # specific processing for: abandon
            COMMAND = 'abandon'
            if parsed_input[1] == COMMAND:
                param_list = parsed_input[2].split(':')
                # length should be exactly 1
                if len(param_list) == 1:
                    # basic parameter value checks: only TN
                    if len(param_list[0]) > 0:
                        ret_dict = {col_command: COMMAND,
                                    col_taskname: param_list[0],
                                    col_taskdesc: '',
                                    col_priolevel: '',
                                    col_percent: ''}

        return ret_dict

    except:
        # no slackbot command match, so return variable is not modified, and is left empty
        return ret_dict


if __name__ == "__main__":

    good_test_lines = ['/slackbot create myTaskA:\'plain vanilla task\':1:10',
                       '/slackbot update myTaskA:::40',
                       '/slackbot update myTaskA:\"new description\"::40',
                       '/slackbot update myTaskA::0:40',
                       '/slackbot update myTaskA:::75',
                       '/slackbot update myTaskA:::100',
                       '/slackbot create myTaskB:\'super duper task\':2:5',
                       '/slackbot update myTaskB:::20',
                       '/slackbot suspend myTaskB',
                       '/slackbot update myTaskB:\'not so super duper task after all\':0:20',
                       '/slackbot update myTaskB:::50',
                       '/slackbot update myTaskB:::100',
                       '/slackbot create myTaskC:\"out of left field task\":1:20',
                       '/slackbot update myTaskC:::40',
                       '/slackbot update myTaskC:::30',
                       '/slackbot update myTaskC::0:30',
                       '/slackbot update myTaskC:::50',
                       '/slackbot update myTaskC:::40',
                       '/slackbot abandon myTaskC'
                      ]

    print('Good test lines:')
    for test_line in good_test_lines:
        print (test_line,':\n   ',slackbot_command_parse(test_line))


    badd_test_lines = ['/slackbott create myTaskA:\'plain vanilla task\':1:10',
                       'slackbot create myTaskA:\'plain vanilla task\':1:10',
                       '/slackbot createmyTaskA:\'plain vanilla task\':1:10',
                       '/slackbotcreate myTaskA:\"plain vanilla task\":1:10',
                       '/slackbot create myTaskA:\"plain vanilla task\":3:10',
                       '/slackbot create myTaskA:\'plain vanilla task\':1:200',
                       '/slackbot create myTaskA:\'plain vanilla task\':1:10:45',
                       '/slackbot create myTaskA:\'plain vanilla task\':hello:10',
                       '/slackbot create myTaskA:\'plain vanilla task\':1:uhuh',
                       '/slackbot create :\'plain vanilla task\':1:uhuh',
                       '/slackbot create :plain vanilla task:1:uhuh',
                       '/slackbot update myTaskA::40',
                       '/slackbot update myTaskA:40',
                       '/slackbot update myTaskA::4:40',
                       '/slackbot update myTaskA:::400',
                       '/slackbot update :::75',
                       '/slackbot suspend myTaskB:::',
                       '/slackbot suspend myTaskB::',
                       '/slackbot suspend myTaskB:',
                       '/slackbot suspend myTaskB:::350',
                       '/slackbot abandon myTaskC:::',
                       '/slackbot abandon myTaskC::',
                       '/slackbot abandon myTaskC:',
                       '/slackbot abandon myTaskC::3:',
                       '/slackbot abandon myTaskC:::102',
                       '/slackbot create myTaskA:\'plain vanilla task\":1:10',
                       '/slackbot create myTaskA:\"plain vanilla task\':1:10'
                       ]

    print()
    print('Bad test lines:')
    for test_line in badd_test_lines:
        print(test_line, ':\n   ', slackbot_command_parse(test_line))
