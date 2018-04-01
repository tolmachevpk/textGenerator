import os
import random
import sys
import time


def check(res, expect, test_name, result_path=None, command=None):
    time.sleep(5)
    if isinstance(res, str):
        res = res.strip()
    elif result_path is not None and os.path.isfile(result_path):
        with open(result_path) as fin:
            res = fin.read().strip()
    try:
        assert res == expect
        print("TEST {0} PASSED:\n COMMAND: {1}\n".format(test_name, command))
    except:
        print("TEST {0} FAILED:\n COMMAND: {3}\n RESULT: {1}\n EXPECTED: {2}\n".format(test_name, res, expect, command))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise IOError('Usage: test.py your_dir_path')
    student = sys.argv[1]

    name = 'badboy'
    if not os.path.isdir(name):
        os.mkdir(name)
        s_boy = "I was! a, bad (((((boy)))))1 "
        s_girl = "She <- is nice) "

        for fold_num in range(1):
            os.mkdir("./{}/{}".format(name, fold_num))
            for text_num in range(2):
                with open("./{2}/{0}/{1}.txt".format(fold_num, text_num, name), 'w') as fout:
                    fout.write((s_boy * random.randint(1, 10000) + '\n') * random.randint(5, 100))

        os.mkdir("./{}/0/girl".format(name))
        for text_num in range(0, 1):
            with open("./{1}/0/girl/{0}.txt".format(text_num, name), 'w') as fout:
                fout.write((s_girl * random.randint(1, 10000) + '\n') * random.randint(5, 100))

    model_path = './{0}/model'.format(student)
    result_path = './{0}/result'.format(student)

    tests = {
        'badboy': [{
            'seed': 'i',
            'length': 10,
            'output': 'i was a bad boy i was a bad boy'
        }, {
            'seed': 'is',
            'length': 5,
            'output': 'is nice she is nice',
        }, {
            'seed': 'I',
            'length': 10,
            'output': 'ERROR'
        }]
    }

    # test pep8
    check(os.popen('pep8 {0}/train.py'.format(student)).read(), '', 'pep8 train')
    check(os.popen('pep8 {0}/generate.py'.format(student)).read(), '', 'pep8 generate')

    for test_case in tests.keys():
        # test for code not failed
        command = 'python {0}/train.py --input-dir ./{2} --model {1} --lc'.format(
            student, model_path,
            test_case
        )
        check(
            os.system(command),
            0,
            'train {} works'.format(test_case),
            command=command
        )

        # test that model is created
        check(os.path.isfile(model_path), True, 'model {} created'.format(test_case))

        # test that model can generate words
        for test_seed in tests[test_case]:
            command = 'python {0}/generate.py --seed {3} --model {1} --length {4} --output {2}'.format(
                student, model_path, result_path,
                test_seed['seed'], test_seed['length']
            )
            if test_seed['output'] != 'ERROR':
                check(
                    os.popen(command),
                    test_seed['output'],
                    'generate {0} on seed "{1}"'.format(test_case, test_seed['seed']),
                    result_path=result_path,
                    command=command
                )
            else:
                check(
                    os.system(command),
                    256,
                    'generate {0} on seed "{1}"'.format(test_case, test_seed['seed']),
                    result_path=None,
                    command=command
                )

            if os.path.isfile(result_path):
                os.remove(result_path)

        if os.path.isfile(model_path):
            os.remove(model_path)

    print("END")