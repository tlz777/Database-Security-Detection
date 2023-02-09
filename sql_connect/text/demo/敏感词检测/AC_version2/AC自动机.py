# ### 方法三：AC自动机
# get_ipython().system('pip install pyahocorasick')
import ahocorasick

def build_actree(wordlist):
    actree = ahocorasick.Automaton()
    for index, word in enumerate(wordlist):
        actree.add_word(word, (index, word))
    actree.make_automaton()
    return actree

if __name__ == '__main__':
    sent = '我草，你是sb吗？狗东西是个什么玩意'
    wordlist = ['我草', '你妈', 'sb', '狗东西']
    actree = build_actree(wordlist=wordlist)
    sent_cp = sent
    for i in actree.iter(sent):
        sent_cp = sent_cp.replace(i[1][1], "**")
        print("屏蔽词：" ,i[1][1])
    print("屏蔽结果：" ,sent_cp)