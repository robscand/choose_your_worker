# coding: utf-8

from random import expovariate 
from math import ceil

class simulation_model:
    def __init__(self, mat_work_exc, mat_work_buld, mat_repair_exc, mat_repair_buld, 
                 num_days_of_model, time_work_in_day):
        self.mw_e = mat_work_exc
        self.mw_b = mat_work_buld
        self.mr_e = mat_repair_exc
        self.mr_b = mat_repair_buld
        
        self.days = num_days_of_model
        self.h = time_work_in_day
        
        self.stat_exc = []
        self.stat_buld = []
        self.symb = []
        
        ## -------------------- Экспоненциальное распределение --------------------
        """Экспоненциальное распределение.

        Лямбда - это 1/мат_ожидание(требуемое среднее значение). Оно должно
        быть ненулевым. Возвращаемые значения варьируются от 0 до бесконечности, 
        если лямбда положительна, и от минус бесконечности до нуля, если лямбда
        отрицательна.
        
        Мы использовали 1-random() вместо random(), чтобы избежать получения логарифма от нуля
        """
        #def expovariate(self, lambd):
        #return -_log(1.0 - self.random())/lambd
        
        ##---------------------------------------------------------------------
        
        self.calculate_time = lambda x: ceil(expovariate(1/x))
        self.get_stats = lambda a, b, c, d: a[b].append(c.count(d))
        pass
    
    def create_model(self, symb_of_work, symb_of_repair, symb_of_delay, inp_my_d,
                     is_print_model = False, is_min_dimension = False):
        self.symb.append(symb_of_work)
        self.symb.append(symb_of_repair)
        self.symb.append(symb_of_delay)
    
        for day in range(self.days):
            w_e = 0
            w_b = 0
            r_e = 0
            r_b = 0

            ct_e = 0
            ct_b = 0
    
            a_e = []
            a_b = []
            #r_str1 = ''
            #r_str2 = ''
            while ct_e < self.h or ct_b < self.h:
                w_e = self.calculate_time(self.mw_e)
                w_b = self.calculate_time(self.mw_b)
                r_e = self.calculate_time(self.mr_e)
                r_b = self.calculate_time(self.mr_b)
        
                #r_str1 += str(t_e)+ ' ' + str(r_e) + ' '
                [a_e.append(self.symb[0]) for i in range(w_e)]
                [a_b.append(self.symb[0]) for i in range(w_b)]
        
                #r_str2 += str(t_b)+ ' ' + str(r_b) + ' '
                [a_e.append(self.symb[1]) for i in range(r_e)]
                [a_b.append(self.symb[1]) for i in range(r_b)]

                ct_e = len(a_e)
                ct_b = len(a_b)
    
            #print(r_str1)
            #print(r_str2)
            del a_e[self.h:]
            del a_b[self.h:]
    
            for i in range(self.h):
                if self.symb[1] in a_e[i] and self.symb[1] in a_b[i]:
                    if self.symb[0] in a_b[i - 1]:
                        a_b.insert(i, self.symb[2])
                    else:
                        a_e.insert(i, self.symb[2])

            del a_e[self.h:]
            del a_b[self.h:]
    
            #Сбор статистики
            self.stat_exc.append([])
            self.stat_buld.append([])
            for j in range(len(self.symb)):
                self.get_stats(self.stat_exc, day, a_e, self.symb[j])
                self.get_stats(self.stat_buld, day, a_b, self.symb[j])
            
            if day == inp_my_d - 1:
                if is_print_model is True:
                    #r_str_e = ''
                    #r_str_b = ''
                    r_str_e = []
                    r_str_b = []
                    cnt1 = 1
                    cnt2 = 0
                    for i in range(1,len(a_e)):
                        if a_e[i] == a_e[i - 1]:
                            cnt1 += 1
                        if a_e[i] != a_e[i - 1]:
                        #Печатаем диапазон от 1, а не от 0, т.е. 16 элементов лежат в диапазоне [1;16]
                            r_str_e.append([])
                            r_str_e[cnt2].append(a_e[i - 1])
                            (r_str_e[cnt2].append(cnt1) if is_min_dimension is True 
                             else r_str_e[cnt2].append(round(cnt1 / 60, 4))) 
                            #r_str_e += str(a_e[i - 1]) + '-' + str(cnt / 60) + '| '
                            cnt1 = 1
                            cnt2 += 1
                    #r_str_e += str(a_e[i - 1]) + '-' + str(cnt / 60) + '| '
                    r_str_e.append([])
                    r_str_e[cnt2].append(a_e[i - 1])
                    (r_str_e[cnt2].append(cnt1) if is_min_dimension is True 
                     else r_str_e[cnt2].append(round(cnt1 / 60, 4))) 
                
                    cnt1 = 1
                    cnt2 = 0
                    for i in range(1,len(a_b)):
                        if a_b[i] == a_b[i - 1]:
                            cnt1 += 1
                        if a_b[i] != a_b[i - 1]:
                            r_str_b.append([])
                            r_str_b[cnt2].append(a_b[i - 1])
                            (r_str_b[cnt2].append(cnt1) if is_min_dimension is True 
                         else r_str_b[cnt2].append(round(cnt1 / 60, 4))) 
                            #r_str_b += str(a_b[i - 1]) + '-' + str(cnt / 60) + '| '  
                            cnt1 = 1
                            cnt2 += 1
                    #r_str_b += str(a_b[i - 1]) + '-' + str(cnt / 60) + '| '
                    r_str_b.append([])
                    r_str_b[cnt2].append(a_b[i - 1])
                    (r_str_b[cnt2].append(cnt1) if is_min_dimension is True 
                     else r_str_b[cnt2].append(round(cnt1 / 60, 4)))
            
                    print('~' * 115)
                    print(day + 1, ' day:')
                
                    print('Excavator data --> ', end = '')
                    print(*r_str_e)
                    print()
                    print('Bulldozer data --> ', end = '')
                    print(*r_str_b)
        pass
    
    #Расчет эффективности
    def economics(self, e_prf, b_prf, e_loss, b_loss, sal, over, is_print_eco = False):
        work_e = 0
        rep_e = 0
        del_e = 0

        work_b = 0
        rep_b = 0
        del_b = 0
        
        prf_e = 0
        prf_b = 0
        #Статистика работы(ремонта, простоя) машин(экскаватора, бульдозера) по всем дням
        for k in range(len(self.stat_exc)):
            work_e += self.stat_exc[k][0] 
            rep_e += self.stat_exc[k][1]
            del_e += self.stat_exc[k][2]
        #print(all_work_exc / 60, all_rep_exc / 60, all_del_exc / 60)

        for k in range(len(self.stat_buld)):
            work_b += self.stat_buld[k][0]
            rep_b += self.stat_buld[k][1]
            del_b += self.stat_buld[k][2]
        #print(all_work_buld / 60, all_rep_buld / 60, all_del_buld / 60)
        
        prf_e = (e_prf * work_e/60 - 
                 ( del_e/60 * e_loss + rep_e/60 * e_loss + rep_e/60 * sal + rep_e/60 * over))
        prf_b = (b_prf * work_b/60 - 
                 ( del_b/60 * b_loss + rep_b/60 * b_loss + rep_b/60 * sal + rep_b/60 * over))
        #print(rep_e/60 * sal + rep_e/60 * over)
        
        if is_print_eco:
            print()
            print('>' * 115)
            print('Статистика за ' + str(self.days) + ' дней:')
            print('1. Прибыль от работы экскаватора: ', ceil(e_prf * work_e/60))
            print('2. Прибыль от работы бульдозера: ', ceil(b_prf * work_b/60))
            print('3. Расходы от времени простоя в ожидании ремонта экскаватора: ', 
                  ceil(del_e/60 * e_loss))
            print('4. Расходы от времени простоя в ожидании ремонта бульдозера: ', 
                  ceil(del_b/60 * b_loss))
            print('5. Расходы от времени простоя во время ремонта экскаватора: ', 
                  ceil(rep_e/60 * e_loss))
            print('6. Расходы от времени простоя во время ремонта бульдозера: ', 
                  ceil(rep_b/60 * b_loss))
            print('7. Палата рабочим (рабочему) за время ремонта экскаватора: ', 
                  ceil(rep_e/60 * sal))
            print('8. Палата рабочим (рабочему) за время ремонта бульдозера: ', 
                  ceil(rep_b/60 * sal))
            print('9. Накладные расходы на бригаду (1 или 2 рабочих)за ремонт экскаватора: ', 
                  ceil(rep_e/60 * over))
            print('10. Накладные расходы на бригаду (1 или 2 рабочих) за ремонт бульдозера: ', 
                  ceil(rep_b/60 * over))
            print('<' * 115)
            print()
        return prf_e + prf_b


if __name__ == '__main__':
    print('Введите, какой день нужно вывести:')
    input_my_day = int(input())

    days = 100
    time = 16 * 60

    mat_e = 4 * 60
    mat_b = 6 * 60

    mat_r_e_6 = 1 * 60
    mat_r_b_6 = 2 * 60

    mat_r_e_63 = 0.25 * 60
    mat_r_b_63 = 1.5 * 60

    s1 = simulation_model(mat_e, mat_b, mat_r_e_63, mat_r_b_63, days, time)
    s1.create_model('W', 'R', 'D', input_my_day, True)

    s2 = simulation_model(mat_e, mat_b, mat_r_e_6, mat_r_b_6, days, time)
    s2.create_model('W', 'R', 'D', input_my_day, True)

    rep_del_exc_loss = 500
    rep_del_buld_loss = 300

    work_exc_profit = 500
    work_buld_profit = 300

    salary_63 = 160
    salary_6 = 100

    overhands = 50

    profit_63 = 0
    profit_6 = 0

    profit_63 = s1.economics(work_exc_profit, work_buld_profit, rep_del_exc_loss, rep_del_buld_loss, 
                         salary_63, overhands, True)
    profit_6 = s2.economics(work_exc_profit, work_buld_profit, rep_del_exc_loss, rep_del_buld_loss, 
                        salary_6, overhands)

    if profit_63 > profit_6:
        print('Рабочего третьего разряда необходимо оставить.')
        print('Так как бригада из двух рабочих эффективнее на ' + str(ceil(profit_63 * 100 / profit_6) - 100) + ' %.')
    else:
        print('Рабочего третьего разряда необходимо уволить.')
        print('Так как бригада из одного рабочего эффективнее на ' + str(ceil(profit_6 * 100 / profit_63) - 100 ) + ' %.')
