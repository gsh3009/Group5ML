import argparse
import random

OUT_DIRECTORY = ""

class question:
    counter = 0

    #question object. Arr is the generated array for the question, correct
    #is the correct ans number. Rest is simple.
    def __init__(self, arr, answer1, answer2, answer3, correct):
        self.arr = arr
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = 'none of the above'
        self.correct = correct

    def toString(self):
        pass
        #print('Question Array: ', self.arr)
        #print('1) ', self.answer1)
        #print('2) ', self.answer2)
        #print('3) ', self.answer3)
        #print('4) ', self.answer4)
        #print('Correct: ', self.correct)


    def generateOutput(self, index, opts):
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
                    output += (subsets_with_num[x] + " " + subsets_with_num[y] + " 0\n")
                    clause_count += 1

        output = "p cnf " + str(len(subsets)) + " " + str(clause_count) + "\n" + output
        #print(output)

        filename = opts.out_dir + str(question.counter) + "_" + str(self.correct == index) + ".dimacs"
        question.counter += 1
        with open(filename, "w") as f:
            f.write(output)


#currently we stop before generating any full size arrays.
def GenCorrectAns(question_arr, size):
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

#generates the subsets for the answer
def GenSubsets(question_arr, size, arrType):
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

#generates all the answers for the question.
def GenAnswers(question_arr, size):
    correctAnsNum = random.randint(1,4)
    answers = []
    for i in range(3):
        curr_size = size
        arrType = random.randint(0,1)
        if i == (correctAnsNum - 1):
            answers.append(GenCorrectAns(question_arr.copy(), curr_size))
        else:
            answers.append(GenSubsets(question_arr.copy(), curr_size, arrType))
    return answers, correctAnsNum

#generates all the questions
def GenTrainData(size, question_num):
    questions = []
    for i in range(question_num):
        question_arr = []
        for j in range(size):
            question_arr.append(j)
        answers, correct = GenAnswers(question_arr,size)
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
        question.toString()
        question.generateOutput(1, opts)
        question.generateOutput(2, opts)
        question.generateOutput(3, opts)


if __name__ == '__main__':
    main()