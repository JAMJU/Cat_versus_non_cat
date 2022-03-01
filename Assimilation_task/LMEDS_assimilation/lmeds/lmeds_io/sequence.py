'''
Created on May 30, 2013

@author: timmahrt
'''

import os
from os.path import join
import io
import random

from lmeds.pages import factories


class TestSetupError(Exception):

    def __init__(self, unknownKeyList, *args, **kargs):
        super(TestSetupError, self).__init__(*args, **kargs)
        self.unknownKeyList = unknownKeyList

    def __str__(self):
        txtString = ("ERROR: The following keys were found in "
                     "'sequence.txt' but they are not associated with any "
                     "pages.  Please consult the test documentation or "
                     "the administrator."
                     )
        unknownKeyStr = "\n".join(self.unknownKeyList)
        
        txtString += "\n" + unknownKeyStr
        
        return txtString


class EndOfTestSequenceException(Exception):
    
    def __init__(self, sequenceFN):
        super(EndOfTestSequenceException, self).__init__()
        self.sequenceFN = sequenceFN
    
    def __str__(self):
        return "End of test sequence: '%s'" % self.sequenceFN


class InvalidFirstLine(Exception):
    
    def __init__(self, item):
        super(InvalidFirstLine, self).__init__()
        self.item = item
        
    def __str__(self):
        return ("ERROR: The first line in a sequence file must be "
                "the sequence title (i.e. start with '*').\n\nFound '%s."
                ) % self.item
    
    
class InvalidSequenceFileError(Exception):
    
    def __init__(self, item):
        super(InvalidSequenceFileError, self).__init__()
        self.item = item
        
    def __str__(self):
        return ("ERROR: The first command in a sequence file cannot be "
                "a subsequence (i.e. start with '#').\n\nFound '%s'."
                ) % self.item


class UnbalancedWrapperError(Exception):
    
    def __init__(self, text, startDelim, endDelim):
        super(UnbalancedWrapperError, self).__init__()
        self.text = text
        self.startDelim = startDelim
        self.endDelim = endDelim
    
    def __str__(self):
        return ("Unbalanced use of %s and %s in string \n %s"
                % (self.startDelim, self.endDelim, self.text))


class UserSequencePathError(Exception):
    
    def __init__(self, path):
        super(UserSequencePathError, self).__init__()
        self.path = path
        
    def __str__(self):
        return ("Path '%s' does not exist in test folder. "
                "Please create it and try again."
                % self.path)

# original version
def _createUserSequence_old(fromFN, toFN):
    title, sequenceList = parseSequence(fromFN, True)
    
    outputSequenceTxt = '*' + title + "\n"
    
    i = 0
    decrement = 0  # Don't count directives
    while i < len(sequenceList):
        if sequenceList[i] == "<randomize>":
            decrement += 1
            outputSequenceTxt += "\n"
            
            # Mark the original order of the stimuli,
            # so we can reconstruct it later
            subList = []
            i += 1
            j = 0
            while True:
                row = sequenceList[i + j]
                if row == "</randomize>":
                    break
                else:
                    subList.append((row, i - decrement + j))
                j += 1
                
            # Randomize order and mark the order this user did the sequence in
            random.shuffle(subList)
            for j, rowTuple in enumerate(subList):
                row, origI = rowTuple
                rowArgs = (row, origI, i - decrement + j)
                outputSequenceTxt += "%s orderSI=%d orderAI=%d\n" % rowArgs
            outputSequenceTxt += "\n"
            i += len(subList)
            
            # Extra 1 for </randomize> tag
            decrement += 1
            i += 1
        
        else:
            row = sequenceList[i]
            outputSequenceTxt += ("%s orderSI=%d orderAI=%d\n" %
                                  (row, i - decrement, i - decrement))
            i += 1
    
    with io.open(toFN, "w", encoding='utf-8') as fd:
        fd.write(outputSequenceTxt)

def get_first_name(filename):
    f = open(filename, 'r')
    first = f.readline().replace('\n', '')
    f.close()
    return first

def remove_first(filename):
    f = open(filename, 'r')
    first = f.readline().replace('\n', '')
    all_rest = f.readlines()
    f.close()
    f = open(filename, 'w')
    f.writelines(all_rest)
    f.close()

def add_to_file(something, filename):
    f = open(filename, 'a')
    f.write(something + '\n')

def get_template_lmeds(file_begin):
    f = open(file_begin, 'r')
    inside = f.readlines()
    f.close()
    return inside

def add_correpondance(corresp, user, sequence):
    f = open(corresp, 'a')
    f.write(user + ':' + sequence + '\n')
    f.close()

def get_corresp(sequence, file_corres):
    f = open(file_corres, 'r')
    all_corres = []
    for line in f:
        new_line = line.replace('\n', '').split(':')
        if len(new_line) > 1:
            if new_line[1] == sequence:
                all_corres.append(new_line[0])
    f.close()
    return all_corres

def get_file_tested(line):
    newline = line.replace('\n', '').split('[[')[-1]
    newline = newline.split(']]')[0]
    return newline

def get_init(line):
    return line.split(',')[0]

def get_answer(line):
    """ We convert the answer from lmeds if vote for 1 (sure : 3, almost sure : 2, unsure 1) idem for 2 but in negative """
    newline = line.replace('\n', '').split(';')[-1].split(',')
    answer_dict = {1:'hibou_cat', 2:'caillou_dog'}
    for i in range(1,7):
        if newline[i] == '1':
            answer = answer_dict[i]
            return answer



def is_ended(file_output):
    """
    Really simple validation, just check that the test is finished
    :param file_output:
    :return:
    """
    end = "text_page,[feedbacks,bindSubmitKeyIDList=,[space]]"
    try:
        f = open(file_output, 'r')
        for line in f:
            if end in line:
                return True
        f.close()
        return False
    except:
        return False

def survey_ok(filename):
    f = open(filename, 'r')
    for line in f:
        if 'presurveyfrench' in line or 'presurveyenglish' in line:
            #print(line)
            newline = line.replace('\n', '').split(';')[1] # we get only the answer to the survey
            #print(newline)
            newline = newline.split(',')
            #print(len(newline))
            dico_answer = {'native_yes':1, 'native_no':2, 'foreign_lang_yes':3, 'foreign_lang_no':4, 'lang_A':5,
                           'lang_B':16, 'lang_C':27, 'lang_D':38, 'expo_infant_yes':49, 'expo_infant_no':50, 'ling_course_yes': 51}

            dico_lang = {}
            for lang in ['lang_A', 'lang_B', 'lang_C', 'lang_D']:
                dico_lang.update({lang + '_expo_' + str(i): dico_answer[lang] + i for i in range(1,6)})
                dico_lang.update({lang + '_level_'+ str(i): dico_answer[lang] + 5 + i for i in range(1,6)})

            dico_answer.update(dico_lang)

            # first is he/she native ?
            if newline[dico_answer['native_no']] == '1':
                return False

            # we do not take the criteria of "feeling native", we suppose it is going to be taken into account in exposition as infant
            """if newline[dico_answer['foreign_lang_yes']] == '1':
                for lang in ['lang_A', 'lang_B', 'lang_C', 'lang_D']:
                    if newline[dico_answer[lang]] != '':
                        # get exposure
                        if newline[dico_answer[lang + '_expo_1']] != '':
                            expo = 0
                            for i in range(1,6):
                                if newline[dico_answer[lang + '_expo_' + str(i)]] == '1':
                                    expo = i
                            if ('presurveyfrench' in line and newline[dico_answer[lang]].lower() != 'français' and expo == 1): # if too much exposure
                                return False
                            if ('presurveyenglish' in line and newline[dico_answer[lang]].lower() != 'english' and expo == 1): # if too much exposure
                                return False

                        # get level
                        if newline[dico_answer[lang + '_level_1']] != '':
                            level = 0
                            for i in range(1,6):
                                if newline[dico_answer[lang + '_level_' + str(i)]] == '1':
                                    level = i
                            if ('presurveyfrench' in line and newline[dico_answer[lang]].lower() != 'français' and level == 1): # if too much exposure
                                return False
                            if ('presurveyenglish' in line and newline[dico_answer[lang]].lower() != 'english' and level == 1): # if too much exposure
                                return False"""

            if newline[dico_answer['expo_infant_yes']] == '1':
                return False
            break
    f.close()
    return True

def test_ok(filename):
    f = open(filename, 'r')
    previous = ""
    answer_test = [] # convert to 1 if good answer, 0 otherwise
    count = 0
    for line in f:
        current = get_init(line)
        if previous == 'media_choice' and current == 'media_choice': # we avoid the beginning test
            file_tested = get_file_tested(line)
            if 'hibou' in file_tested or 'caillou' in file_tested or 'dog' in file_tested or 'cat' in file_tested: # test file names
                answer_indiv = get_answer(line)
                pos1 = answer_indiv.split('_')[0]
                pos2 = answer_indiv.split('_')[1]
                #gold_answer = get_gold_answer_test(file_tested, answer_test_easy)
                answer_test.append(1 if (pos1 in file_tested or pos2 in file_tested) else 0)
                count += 1
        previous = current
    summ = sum(answer_test)
    if count - summ <= 1:
        return True
    else:
        return False


def is_validated(file_output):
    """
    Check that is ended, is native, no language for which is native, no exposure when kid, no linguistic course and check less than two errors in test
    :param file_output:
    :return:
    """
    try:
        #print(file_output, is_ended(file_output), survey_ok(file_output), test_ok(file_output))
        if not is_ended(file_output):
            return False
        if not survey_ok(file_output):
            return False
        if not test_ok(file_output):
            return False
        return True
    except:
        return False



def check_all_files(corres, to_do, done, temp, ouput_path):
    # first we check every files in temp
    temp_file = open(temp, 'r')
    # we keep this in temp, and we will check which one to add to to_do
    still_to_do = []
    # we will add this to done
    done_list = []
    for line in temp_file:
        new_line = line.replace('\n', '')
        users = get_corresp(sequence=new_line, file_corres=corres)
        if users == []:
            still_to_do.append(new_line)
        else:
            valid = False
            for user in users:
                valid = valid or is_validated(os.path.join(ouput_path, user + '.csv'))
            if not valid:
                still_to_do.append(new_line)
            else:
                done_list.append(new_line)

    temp_file.close()
    # first we add what we need to add to done
    for file in done_list:
        add_to_file(file, done) # we add the file done to done

    # then we remove the done from temp
    temp_file = open(temp, 'r')
    lines_temp = temp_file.readlines()
    temp_file.close()
    temp_file = open(temp, 'w')
    for line in lines_temp:
        new_line = line.replace('\n', '')
        if not new_line in done_list:
            temp_file.write(line)
    temp_file.close()

    # then we put the still to do in to_do and remove done from to_do
    to_do_file = open(to_do, 'r')
    lines_temp = to_do_file.readlines()
    to_do_file.close()
    to_do_file = open(to_do, 'w')
    already_in = []
    for line in lines_temp:
        new_line = line.replace('\n', '')
        if not new_line in done_list:
            to_do_file.write(line)
            already_in.append(new_line)

    # we add the sequence that are missing
    for to_add in still_to_do:
        if not to_add in already_in:
            to_do_file.write(to_add + '\n')
    to_do_file.close()

# new version for pilote and real test
def _createUserSequence(fromFN, toFN):
    title, sequenceList = parseSequence(fromFN, True)


    sequencePath = os.path.split(fromFN)[0]
    user = toFN.split('/')[-1]
    all_sequences_path = os.path.join(sequencePath, title + '_list_sequences/')
    # contains all the name of sequences not tested at all
    to_do = os.path.join(all_sequences_path, 'to_do.txt')
    # contains all the name of sequences that are done and validated
    done = os.path.join(all_sequences_path, 'done.txt')
    # contains all the name of sequences not validated
    temp = os.path.join(all_sequences_path, 'temp.txt')
    # correpondance between sequence:user.txt
    corresp = os.path.join(all_sequences_path, 'correspondance.txt')

    # first we check the files and outputs to validate outputs and change lists
    check_all_files(corres=corresp, to_do = to_do, done = done, temp = temp, ouput_path = os.path.join(sequencePath, 'output', title))

    # we get the name of file that is on top
    name = get_first_name(to_do)
    if name == "":
        name = get_first_name(temp)
        if name == "":
            name = "sequence_nulle" # we load the null sequence that says we have enough participants

    else:
        remove_first(to_do)

    outputSequenceTxt = get_template_lmeds(os.path.join(all_sequences_path, name + '.txt'))
    add_correpondance(corresp, user[:-4], name)
    with io.open(toFN , "w", encoding='utf-8') as fd:
        fd.writelines(outputSequenceTxt)
    #return new_name

class TestSequence(object):
    
    def __init__(self, webSurvey, sequenceFN, individualSequenceName=None):

        if individualSequenceName is not None:
            sequencePath = os.path.split(sequenceFN)[0]
            
            # Loading the sequence title -- dropping the '*' prefix
            with io.open(sequenceFN, "r", encoding='utf-8') as fd:
                sequenceTitle = fd.readline().strip()[1:]
            
            newPath = join(sequencePath, "individual_sequences", sequenceTitle)
            
            if not os.path.exists(newPath):
                raise UserSequencePathError(join("<test_root>",
                                                 "individual_sequences",
                                                 sequenceTitle))
            
            newSequenceFN = join(newPath, individualSequenceName + ".txt")
            if not os.path.exists(newSequenceFN):
                # change that # _createUserSequence(sequenceFN, newSequenceFN)
                _createUserSequence(sequenceFN, newSequenceFN)
            # change that # sequenceFN = newSequenceFN
            sequenceFN = newSequenceFN
        
        self.sequenceFN = sequenceFN
    
        self.webSurvey = webSurvey  # Needed to instantiate pages
        self.sequenceTitle, self.testItemList = parseSequence(sequenceFN)
    
    def getNumPages(self):
        return len(self.testItemList)
        
    def getPage(self, pageNum):
        pageName, argList, kargDict = getPageArgs(self.testItemList[pageNum])
        page = factories.loadPage(self.webSurvey, pageName, argList, kargDict)
        
        return page

    def getPageStr(self, pageNum):
        pageRow = self.testItemList[pageNum]
        
        chunkList = recChunkLine(pageRow)
        pageName = chunkList.pop(0)
        
        return pageName, chunkList


def parseSequence(sequenceFN, keepDirectives=False):
    with io.open(sequenceFN, "r", encoding='utf-8') as fd:
        testItemList = [row.rstrip("\n") for row in fd.readlines()]
    testItemList = [row for row in testItemList if row != '']
    
    if keepDirectives is False:
        testItemList = [row for row in testItemList if row[0] != '<']

    # Validate the test title
    sequenceTitle = testItemList.pop(0)
    if sequenceTitle[0] != "*":
        raise InvalidFirstLine(sequenceTitle)
    
    # Now that we've validated this is the sequence title,
    # get rid of the '*'
    sequenceTitle = sequenceTitle[1:]

    return sequenceTitle, testItemList


def _parse(txt, startDelim, endDelim, startI):
    '''
    For embedded structures, finds the appropriate start and end of one
    
    Given:
    [[0 0] [0 1] ] [2 3 4]
    This would return the indicies for:
    [[0 0] [0 1] ]
    > (0, 13)
    '''
    endI = None
    depth = 0
    startI = txt.index(startDelim, startI)
    for i in range(startI, len(txt)):
        if txt[i] == startDelim:
            depth += 1
        elif txt[i] == endDelim:
            depth -= 1
            if depth == 0:
                endI = i + 1
                break
    
    if endI is None:
        raise UnbalancedWrapperError(txt, startDelim, endDelim)
    
    return startI, endI


def _splitTxt(txt, splitItem):
    '''
    Split on whitespace or splitItem
    '''
    if splitItem is None:
        tmpDataList = txt.split()
    else:
        tmpDataList = txt.split(splitItem)
        tmpDataList = [row.strip() for row in tmpDataList if row.strip() != ""]
        
    return tmpDataList


def getPageArgs(pageRow):
    
    pageArgStr = recChunkLine(pageRow)
    pageName = pageArgStr.pop(0)
    
    # Get non-keyword arguments
    argList = []
    while len(pageArgStr) > 0:
        if '=' not in pageArgStr[0]:
            argList.append(pageArgStr.pop(0))
        else:
            break
    
    # Get keyword arguments
    kargDict = {}
    while len(pageArgStr) > 0:
        if len(pageArgStr) > 1 and isinstance(pageArgStr[1], type([])):
            key = pageArgStr.pop(0).split("=", 1)[0]
            value = pageArgStr.pop(0)
        else:
            key, value = pageArgStr.pop(0).split("=", 1)
        kargDict[key] = value
        
    return pageName, argList, kargDict


def recChunkLine(line, splitItem=None):
    '''
    Parses a line on space or splitItem.  Handles embedded lists.
    
    Given:
    a b c [d e f] [[g] h]
    Returns:
    ['a', 'b', 'c', ['d', 'e', 'f'], [['g'], 'h']]
    '''
    
    indicies = [0]
    indexList = []
    startIndex = 0
    endIndex = 0
    char1 = "["
    char2 = "]"
    while True:

        try:
            bracketStartIndex, endIndex = _parse(line, char1, char2,
                                                 startIndex)
        except ValueError:
            break
        
        indexList.append((startIndex, bracketStartIndex))
        indexList.append((bracketStartIndex, endIndex))
        
        indicies.append(endIndex)
        startIndex = endIndex
    
    if endIndex == 0:
        indexList.append((0, -1))
    else:
        indexList.append((endIndex, -1))
    
    # Make chunks
    chunkList = []
    i = 0
    while i < len(indexList) - 1:
        tmpData = line[indexList[i][0]:indexList[i][1]].strip()
        if char1 in tmpData:
            chunkList.append(recChunkLine(tmpData[1:-1], splitItem))
        elif tmpData != "":
            chunkList.extend((_splitTxt(tmpData, splitItem)))
        i += 1
    tmpData = line[indexList[-1][0]:].strip()
    if tmpData != "":
        splitData = _splitTxt(tmpData, splitItem)
        if splitData[0] == tmpData:
            splitData = _splitTxt(tmpData, None)
        chunkList.extend(splitData)
    
    return chunkList
