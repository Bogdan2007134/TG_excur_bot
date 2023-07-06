var_scenario = ["Военный сюжет",
                ["""Мы находимся на главной площади Волгограда, и начинаем\nпутешествие по городу-герою в прошлом Сталинград""", "volgograd\Var_scenario\photo_1.png","volgograd\Var_scenario\map_1.png"],
                ["""Если мы пройдем туда то и туда то\nто мы увидим тото и тото""", 'volgograd\Var_scenario\photo_2.png', "volgograd\Var_scenario\map_2.png"],
                ["""А если пройдем еще дальше то\nувидим Родину-Мать""", "volgograd\Var_scenario\photo_3.png", "volgograd\Var_scenario\map_3.png"],
                ["""Вот наша экскурсия\nи подошла к концу""", 'volgograd\Var_scenario\photo_4.png', "volgograd\Var_scenario\map_4.png"]
                ]
romantic_scenario = ["Романтический сюжет",
                    ["""Мы находимся на главной площади Волгограда,\nи начинаем путешествие по романтичному городу\nгде творила Котова Анна Геннадьевна""", "volgograd\Rom_scenario\photo_1.png", "volgograd\Rom_scenario\map_1.png"],
                    ["""Если мы пройдем туда то и туда то\nто мы увидим тото и тото""","volgograd\Rom_scenario\photo_2.png", "volgograd\Rom_scenario\map_2.png"],
                    ["""А если пройдем еще дальше то\nувидим Родину-Мать""","volgograd\Rom_scenario\photo_3.png", "volgograd\Rom_scenario\map_3.png"],
                    ["""Вот наша экскурсия\nи подошла к концу""","volgograd\Rom_scenario\photo_4.png", "volgograd\Rom_scenario\map_4.png"]
                    ]
interactiv_scenario = [[["Интерактивный сюжет"]],
                       [["Сюжетная линия №0",'volgograd\Test_interactiv\scenario_0.1.png', "True"]],
                       [["Сюжетная линия №0",'volgograd\Test_interactiv\scenario_0.2.png'],["Сюжетная линия №1",'volgograd\Test_interactiv\scenario_1.2.png'],["Сюжетная линия №2",'volgograd\Test_interactiv\scenario_2.2.png']],  
                       [["Сюжетная линия №0",'volgograd\Test_interactiv\scenario_0.3.png'],["Сюжетная линия №1",'volgograd\Test_interactiv\scenario_1.3.png'],["Сюжетная линия №2",'volgograd\Test_interactiv\scenario_2.3.png']],
                       [["Сюжетная линия №0",'volgograd\Test_interactiv\scenario_0.4.png'],["Сюжетная линия №1",'volgograd\Test_interactiv\scenario_1.4.png'],["Сюжетная линия №2",'volgograd\Test_interactiv\scenario_2.4.png']],
                      ]
volgograd_list = [var_scenario[0], romantic_scenario[0], interactiv_scenario[0][0][0]]
volgograd = {"Военныйсюжет": var_scenario,
             "Романтическийсюжет": romantic_scenario,
             "Интерактивныйсюжет": interactiv_scenario,}
