from unittest import TestCase, main
from diff import *
class Test_diff(TestCase):

    def test_diffset(self):
        A = set(['1','2'])
        B = set(['1','2'])
        C1,C2 = diffset(A,B)
        self.assertEquals(len(C1),0)
        self.assertEquals(len(C2),0)

        A = set(['3','2'])
        B = set(['2'])
        C1,C2 = diffset(A,B)
        self.assertEquals(len(C1),0)
        self.assertEquals(len(C2),1) 

        A = set(['1','3','5','7'])
        B = set(['1','2','4'])
        C1,C2 = diffset(A,B)
        self.assertEquals(len(C1),2)
        self.assertEquals(len(C2),3) 

    

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass