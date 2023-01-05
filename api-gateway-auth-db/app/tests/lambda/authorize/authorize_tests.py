import json
import unittest
import sys
import os



class MyTestCase(unittest.TestCase):
    

    def test_scope_jwt(self):
        scopes = "['admin', 'user', 'super-user']"
    

        scopes = scopes.replace("[", "").replace("]", "").replace("'", "").strip()
        scopes = scopes.split(",")
        
        # strip the spaces
        scopes = [x.strip() for x in scopes]
       



        self.assertEquals(3, len(scopes))

        self.assertEquals("admin", scopes[0])
        self.assertEquals("user", scopes[1])
        self.assertEquals("super-user", scopes[2])


    

    
if __name__ == '__main__':
    print(f'dir: {__file__}')
    unittest.main()