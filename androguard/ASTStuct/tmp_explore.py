method_ast_str = '''
{'body': ['BlockStatement',
          None,
          [['LocalDeclarationStatement',
            ['MethodInvocation',
             [['TypeName', ('android/net/Uri', 0)], ['Local', 'p6']],
             ('android/net/Uri',
              'parse',
              '(Ljava/lang/String;)Landroid/net/Uri;'),
             'parse',
             True],
            [['TypeName', ('android/net/Uri', 0)], ['Local', 'v0']]],
           ['IfStatement',
            None,
            ['Unary',
             [['MethodInvocation',
               [['Local', 'p6'],
                ['Literal', 'micloud:', ('java/lang/String', 0)]],
               ('java/lang/String', 'startsWith', '(Ljava/lang/String;)Z'),
               'startsWith',
               True]],
             '!',
             False],
            [['BlockStatement',
              None,
              [['IfStatement',
                None,
                ['Unary',
                 [['MethodInvocation',
                   [['Literal', '/cloudservice/home', ('java/lang/String', 0)],
                    ['MethodInvocation',
                     [['Local', 'v0']],
                     ('android/net/Uri', 'getPath', '()Ljava/lang/String;'),
                     'getPath',
                     True]],
                   ('java/lang/String', 'equals', '(Ljava/lang/Object;)Z'),
                   'equals',
                   True]],
                 '!',
                 False],
                [['BlockStatement',
                  None,
                  [['IfStatement',
                    None,
                    ['Unary',
                     [['MethodInvocation',
                       [['Literal',
                         '/cloudservice/browse',
                         ('java/lang/String', 0)],
                        ['MethodInvocation',
                         [['Local', 'v0']],
                         ('android/net/Uri', 'getPath', '()Ljava/lang/String;'),
                         'getPath',
                         True]],
                       ('java/lang/String', 'equals', '(Ljava/lang/Object;)Z'),
                       'equals',
                       True]],
                     '!',
                     False],
                    [['BlockStatement',
                      None,
                      [['ReturnStatement',
                        ['MethodInvocation',
                         [['Local', 'super'], ['Local', 'p5'], ['Local', 'p6']],
                         ('com/miui/cloudservice/hybrid/k',
                          'shouldOverrideUrlLoading',
                          '(Lmiui/hybrid/HybridView;Ljava/lang/String;)Z'),
                         'shouldOverrideUrlLoading',
                         True]]]],
                     ['BlockStatement',
                      None,
                      [['ExpressionStatement',
                        ['MethodInvocation',
                         [['Local', 'this'], ['Local', 'p5'], ['Local', 'v0']],
                         ('com/miui/cloudservice/ui/MiCloudHybridActivity$a',
                          'a',
                          '(Lmiui/hybrid/HybridView;Landroid/net/Uri;)V'),
                         'a',
                         True]],
                       ['ReturnStatement', ['Literal', '1', ('.int', 0)]]]]]]]],
                 ['BlockStatement',
                  None,
                  [['ExpressionStatement',
                    ['MethodInvocation',
                     [['Local', 'this']],
                     ('com/miui/cloudservice/ui/MiCloudHybridActivity$a',
                      'a',
                      '()V'),
                     'a',
                     True]],
                   ['ReturnStatement', ['Literal', '1', ('.int', 0)]]]]]]]],
             ['BlockStatement',
              None,
              [['LocalDeclarationStatement',
                ['MethodInvocation',
                 [['Local', 'v0']],
                 ('android/net/Uri', 'getAuthority', '()Ljava/lang/String;'),
                 'getAuthority',
                 True],
                [['TypeName', ('com/miui/cloudservice/hybrid/z', 0)],
                 ['Local', 'v6_1']]],
               ['IfStatement',
                None,
                ['BinaryInfix',
                 [['Local', 'v6_1'], ['Literal', 'null', ('.null', 0)]],
                 '=='],
                [['BlockStatement',
                  None,
                  [['ThrowStatement',
                    ['ClassInstanceCreation',
                     [['Literal',
                       'Null action for deep link start with micloud:// !',
                       ('java/lang/String', 0)]],
                     ['TypeName',
                      ('java/lang/IllegalArgumentException', 0)]]]]],
                 ['BlockStatement',
                  None,
                  [['IfStatement',
                    None,
                    ['Unary',
                     [['MethodInvocation',
                       [['Local', 'v6_1'],
                        ['Literal', 'share', ('java/lang/String', 0)]],
                       ('java/lang/String',
                        'equalsIgnoreCase',
                        '(Ljava/lang/String;)Z'),
                       'equalsIgnoreCase',
                       True]],
                     '!',
                     False],
                    [['BlockStatement',
                      None,
                      [['IfStatement',
                        None,
                        ['MethodInvocation',
                         [['Local', 'v6_1'],
                          ['Literal', 'feedback', ('java/lang/String', 0)]],
                         ('java/lang/String',
                          'equalsIgnoreCase',
                          '(Ljava/lang/String;)Z'),
                         'equalsIgnoreCase',
                         True],
                        [['BlockStatement',
                          None,
                          [['ExpressionStatement',
                            ['MethodInvocation',
                             [['TypeName',
                               ('com/miui/cloudservice/ui/MiCloudHybridActivity',
                                0)],
                              ['FieldAccess',
                               [['Local', 'this']],
                               ('com/miui/cloudservice/ui/MiCloudHybridActivity$a',
                                'c',
                                'Lcom/miui/cloudservice/ui/MiCloudHybridActivity;')]],
                             ('com/miui/cloudservice/ui/MiCloudHybridActivity',
                              'a',
                              '(Landroid/content/Context;)V'),
                             'a',
                             True]]]]]]]],
                     ['BlockStatement',
                      None,
                      [['ExpressionStatement',
                        ['MethodInvocation',
                         [['MethodInvocation',
                           [['TypeName',
                             ('com/miui/cloudservice/ui/MiCloudHybridActivity',
                              0)],
                            ['FieldAccess',
                             [['Local', 'this']],
                             ('com/miui/cloudservice/ui/MiCloudHybridActivity$a',
                              'c',
                              'Lcom/miui/cloudservice/ui/MiCloudHybridActivity;')]],
                           ('com/miui/cloudservice/ui/MiCloudHybridActivity',
                            'a',
                            '(Lcom/miui/cloudservice/ui/MiCloudHybridActivity;)Lcom/miui/cloudservice/hybrid/z;'),
                           'a',
                           True]],
                         ('com/miui/cloudservice/hybrid/z', 'b', '()V'),
                         'b',
                         True]],
                       ['ExpressionStatement',
                        ['MethodInvocation',
                         [['Local', 'this'], ['Local', 'p5'], ['Local', 'v0']],
                         ('com/miui/cloudservice/ui/MiCloudHybridActivity$a',
                          'b',
                          '(Lmiui/hybrid/HybridView;Landroid/net/Uri;)V'),
                         'b',
                         True]]]]]],
                   ['ReturnStatement', ['Literal', '1', ('.int', 0)]]]]]]]]]]]],
 'comments': [],
 'flags': ['public'],
 'params': [[['TypeName', ('miui/hybrid/HybridView', 0)], ['Local', 'p5']],
            [['TypeName', ('java/lang/String', 0)], ['Local', 'p6']]],
 'ret': ['TypeName', ('.boolean', 0)],
 'triple': ('com/miui/cloudservice/ui/MiCloudHybridActivity$a',
            'shouldOverrideUrlLoading',
            '(Lmiui/hybrid/HybridView;Ljava/lang/String;)Z')}
'''

import json

# method_ast_str = method_ast_str.replace('\'','\"')
# method_ast = json.loads(method_ast_str)
method_ast = eval(method_ast_str)
method_params = method_ast['params']
method_ret = method_ast['ret']

print("#### Log parase pararms ####")
print(str(type(method_params))+'  --->   '+str(method_params))
for param in method_params:
  print(str(param))

# print("#### Log two ####")
# for params in method_params:
#     print(str(params))