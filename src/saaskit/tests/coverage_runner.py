### -*- coding: utf-8 -*- ####################################################
"""
=========   given from http://alarin.blogspot.com/ ===========
Test runner with code coverage.
Falls back to django simple runner if coverage-lib not installed 

$Id:interfaces.py 11316 2008-05-19 12:07:19Z arvid $
"""

import os

from django.test import simple
from django.conf import settings


#попытка импорта coverage библиотеки
try:
    from coverage import coverage as Coverage
except ImportError:
#если она не установлена, просто запустим стандартный обработчик
    run_tests = simple.run_tests 
else:
#если установлена примемся за построение отчета
    coverage = Coverage()
    def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):

# часть непосредственно отвечающая за получение данных о покрытии (включить сбор; выполнить тесты; выключить сбор)
        coverage.start()
        test_results = simple.run_tests(test_labels, verbosity, interactive, extra_tests)
        coverage.stop()

# Как известно, manage.py test может не все тесты, а только из определенных приложений
# немного не логично, что в этом случае покрытие будет определено для всего кода в проекте
# и для не ваших приложений и для библиотек.
# Следующий код берет имена приложений для тестирования из test_labels, определяет все модули
# входящие в их состав и передает список для построения отчета.
# Это очень удобно, мы тестируем только свой код и получаем только его покрытие.
        coverage_modules = []
        for app in test_labels:
            try:
                module = __import__(app, globals(), locals(), [''])
            except ImportError:
# Эта ситуация возникает в случае если тестирование ограничено одним TestCase, либо модуль недоступен
# В обоих случая нам не нужен отчет о покрытии.
                coverage_modules = None
                break
            if module:
                base_path = os.path.join(os.path.split(module.__file__)[0], "")
# Ищем внутри приложения непустые .py файлы
                for root, dirs, files in os.walk(base_path):
                    for fname in files:
                        if fname.endswith(".py") and os.path.getsize(os.path.join(root, fname)) > 1:
                            try:
                                mname = os.path.join(app, os.path.join(root, fname).replace(base_path, "")) 
                                coverage_modules.append(mname)
                            except ImportError:
                                pass #do nothing
        
# Строим html-отчет        
        if coverage_modules or not test_labels:
            coverage.html_report(coverage_modules, directory=settings.COVERAGE_REPORT_PATH)
                    
        return test_results
