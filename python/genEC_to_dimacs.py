import argparse
import random

#OUT_DIRECTORY = ""

'''
The class that manages data for solving exact cover problems. Used in problem generation
to ensure that problems have the correct true class.
'''
class exactCoverSolver:
    subset_sizes = []  # current list of subset sizes

    def solve(self, main_set_as_list, subsets):
        '''
        Function that solves an exact cover problem.
        self: An exactCoverSolver object.
        main_set_as_list: The target set of the exact cover problem, stored as a list.
        subsets: The list of subsets (which are stored as sets).
        '''
        main_set = set(main_set_as_list)
        main_set_size = len(main_set)
        exactCoverSolver.subset_sizes = []
        for x in range(0, len(subsets)):
            exactCoverSolver.subset_sizes.append(len(subsets[x]))

        combos_to_check = self.get_combos_rec(0, main_set_size)

        for combo in combos_to_check:
            union_of_combo = set()
            for index in combo:
                union_of_combo = set.union(union_of_combo, subsets[index])
            if len(union_of_combo) == len(main_set):
                return True

        return False

    def get_combos_rec(self, index, remaining_size):
        '''
        Recursive function that gets all combinations of the remaining subsets (the subsets after the 
        index parameter) that add up to the size of the target set.
        self: An exactCoverSolver object.
        index: The index of the set we are responsible for.
        remaining_size: The size of the target set, minus the size of all previously included subsets.
        '''
        valid_combos = []

        if remaining_size < 0:
            return []

        if index == len(exactCoverSolver.subset_sizes):
            return []

        if index == len(exactCoverSolver.subset_sizes) - 1 and remaining_size == 0:
            return [[]]
        elif index == len(exactCoverSolver.subset_sizes) - 1 and remaining_size == exactCoverSolver.subset_sizes[index]:
            return [[index]]

        with_us = self.get_combos_rec(index + 1, remaining_size - exactCoverSolver.subset_sizes[index])
        for combo in with_us:
            combo.append(index)
            valid_combos.append(combo)
        without_us = self.get_combos_rec(index + 1, remaining_size)
        for combo in without_us:
            valid_combos.append(combo)

        return valid_combos


def GenerateRandomSubset(main_set_list):
    '''
    Generates a random subset of the provided main set.
    main_set_list: The main set (stored as a list).
    '''
    subset = set()
    while len(subset) == 0:
        for x in range(0, len(main_set_list)):
            if random.random() < 0.5:
                subset.add(main_set_list[x])
    return subset


def GenerateProblem(main_set_as_list, answer):
     '''
    Generates an exact cover problem.
    main_set_as_list: The main set that will be used for the problem (stored as a list).
    answer: The intended answer for the problem (True or False)
    '''
    solver = exactCoverSolver()

    # main_set_as_list = [0, 1, 2, 3, 4]
    subsets = []
    done = False
    while not done:
        subsets.append(GenerateRandomSubset(main_set_as_list))
        done = solver.solve(main_set_as_list, subsets)

    if answer:  # == True
        random.shuffle(subsets)
        return subsets
        # return main_set_as_list, subsets
    else:
        subsets.pop(-1)
        return subsets
        # return main_set_as_list, subsets

class question:
    '''
    Object used to store all the information of a generated problem
    arr: Array of randomly generated numbers that 
         serves as the base for the Exact Cover Problem
    answer1-3: 3 randomly generated arrays of subsets.
    answer4: none satisfiable questoin
    correct: correct answer for that subset
    '''
    counter = 0

    
    def __init__(self, arr, answer1, answer2, answer3, correct):
        self.arr = arr
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = 'none of the above'
        self.correct = correct


    def generateOutput(self, index, opts):
        '''
        Generates the output file for the exact cover problem with the given index
        index: The index of the problem to export.
        opts: The options passed into the program, used to find the output directory.
        '''
        if index == 1:
            subsets = self.answer1
        elif index == 2:
            subsets = self.answer2
        else:
            subsets = self.answer3

        output = ""

        clause_count = 0

        for num in self.arr:
            subsets_with_num = []
            for x in range(0, len(subsets)):
                subset = subsets[x]
                if num in subset:
                    subsets_with_num.append(str(x+1))  # IDs need to start from 1 because 0 is used to end clauses

            if len(subsets_with_num) == 0:  # if there are no subsets with the number...
                output += "1 0\n-1 0\n"  # an exact cover is impossible, so create a contradiction (A and not A)
                clause_count += 2
                continue

            for subset_id in subsets_with_num:
                output += (subset_id + " ")
            output += "0\n"
            clause_count += 1

            for x in range(0, len(subsets_with_num)):
                for y in range(x+1, len(subsets_with_num)):
                    output += ("-" + subsets_with_num[x] + " " + "-" + subsets_with_num[y] + " 0\n")
                    clause_count += 1

        output = "p cnf " + str(len(subsets)) + " " + str(clause_count) + "\n" + output

        filename = opts.out_dir + str(question.counter) + "_" + str(self.correct == index) + ".dimacs"
        question.counter += 1
        with open(filename, "w") as f:
            f.write(output)

def GenCorrectAns(question_arr, size):
    '''
    Generates an exact cover of the question array using randomly generated subsets
    question_array: Array of randomly generated numbers that 
                    serves as the base for the Exact Cover Problem
    answer: an exact cover of the question array created with randomly generated subsets
    '''
    answer = []
    while size > 0:
        subset_size = random.randint(1, size)
        curr_subset = []
        size = size - subset_size
        for i in range(subset_size):
            rand_index = random.randint(0, size)
            curr_subset.append(question_arr[rand_index])
            del question_arr[rand_index]
        answer.append(curr_subset)
    return answer


def GenSubsets(question_arr, size, arrType):
    '''
    Generates random subsets for the Exact Cover Problem
    question_array: Array of randomly generated numbers that 
                    serves as the base for the Exact Cover Problem
    size: integer size of question_array
    arrType: boolean value to see if subsets should remove values from the array
             or not
    answer: returns a list of generated subsets.
    '''
    answer = []
    while size > 0:
        subset_size = random.randint(1, size)
        curr_subset = []
        if size - subset_size == 0 and arrType == 0:
            subset_size -= 1
            size = 0
        else:
            size = size - subset_size
        if(subset_size == 0):
            return answer
        for i in range(subset_size):
            rand_index = random.randint(0, size)
            curr_subset.append(question_arr[rand_index])
            if arrType == 0:
                del question_arr[rand_index]
        answer.append(curr_subset)
    return answer

def GenAnswers(question_array):
    '''
    Generates the answers for the Exact Cover Problem
    question_array: Array of randomly generated numbers that 
                    serves as the base for the Exact Cover Problem
    answers: returns the an array of answers to the exact cover problem
    correctAnsNum: returns which number is the correct answer
    '''
    correctAnsNum = random.randint(1,4)
    answers = []
    for i in range(3):
        if i == (correctAnsNum - 1):
            answers.append(GenerateProblem(question_array, True))
        else:
            answers.append(GenerateProblem(question_array, False))
    return answers, correctAnsNum


def GenTrainData(size, question_num):
    '''
    Generates the Exact Cover Problem Questions
    size: integer representing the size of the array
    quesiton_num: integer representing the amount of questions to be generated
    '''
    questions = []
    for i in range(question_num):
        question_arr = []
        for j in range(size):
            question_arr.append(j)
        answers, correct = GenAnswers(question_arr)
        q = question(question_arr, answers[0], answers[1], answers[2], correct)
        questions.append(q)
    return questions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('out_dir', action='store', type=str)
    parser.add_argument('--problem_size', action='store', dest='problem_size', type=int, default=10)
    parser.add_argument('--question_num', action='store', dest='question_num', type=int, default=10)
    opts = parser.parse_args()
    questions = GenTrainData(opts.problem_size, opts.question_num)
    for question in questions:
        #question.toString()
        question.generateOutput(1, opts)
        question.generateOutput(2, opts)
        question.generateOutput(3, opts)


if __name__ == '__main__':
    main()
