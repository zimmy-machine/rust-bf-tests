import os
import datetime

test_dir = "tests/"
test_names = os.popen("find "  + test_dir  + "*.bf | sed 's/\.[^.]*$//'").read().split('\n')[:-1]

bf_names = [test + ".bf" for test in test_names]
in_names = [test + ".in" for test in test_names]
ok_names = [test + ".ok" for test in test_names]

test_case_xml = []

num_failed = 0
for i in range(len(bf_names)):
    output = os.popen("(test -f " + in_names[i] + " || timeout 5 cargo run " + bf_names[i] + " 1) && \
                        timeout 5 cargo run " + bf_names[i] + " 1 < " + in_names[i]).read().rstrip()
    answer = open(ok_names[i], 'r').read().rstrip()
    
    if output == answer:
        test_case_xml.append(f"<testcase name=\"{bf_names[i]}\" classname=\"tests\" time=\"0\">" + \
                            f"<system-out>{output}</system-out></testcase>")
    else:
        num_failed = num_failed + 1
        test_case_xml.append(f"<testcase name=\"{bf_names[i]}\" classname=\"tests\" time=\"0\">" + \
                            f"<failure type=\"cargo test\" message=\"{output}\"/></testcase>")

header = "<testsuites>\n" + \
"<testsuite id=\"0\" name=\"cargo test #0\" package=\"testsuite/cargo test #0\" " + \
f"tests=\"{len(bf_names)}\" errors=\"0\" failures=\"{num_failed}\" hostname=\"localhost\" timestamp=\"{datetime.datetime.now()}\"" + \
" time=\"0\">"

footer = "</testsuite>\n</testsuites>"

xml_output = header
for tc in test_case_xml:
    xml_output += tc
xml_output += footer

if not os.path.exists('test-results'):
    os.mkdir("test-results")
if not os.path.exists('test-results/rust'):
    os.mkdir("test-results/rust")

print(xml_output)

open('test-results/rust/results.xml', 'w').write(xml_output)

if num_failed != 0:
    exit(101)
