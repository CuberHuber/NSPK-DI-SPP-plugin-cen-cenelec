"""
Парсер плагина SPP

1/2 документ плагина
"""
import datetime
import logging
import os
import time

from src.spp.types import SPP_document


class CEN_CENELEC:
    """
    Класс парсера плагина SPP

    :warning Все необходимое для работы парсера должно находится внутри этого класса

    :_content_document: Это список объектов документа. При старте класса этот список должен обнулиться,
                        а затем по мере обработки источника - заполняться.


    """

    SOURCE_NAME = 'cen&cenelec'
    HOST = 'https://standards.cencenelec.eu'
    _content_document: list[SPP_document]

    def __init__(self, *args, **kwargs):
        """
        Конструктор класса парсера

        По умолчанию внего ничего не передается, но если требуется (например: driver селениума), то нужно будет
        заполнить конфигурацию
        """
        # Обнуление списка
        self._content_document = []

        # Логер должен подключаться так. Вся настройка лежит на платформе
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"Parser class init completed")
        self.logger.info(f"Set source: {self.SOURCE_NAME}")
        ...

    def content(self) -> list[SPP_document]:
        """
        Главный метод парсера. Его будет вызывать платформа. Он вызывает метод _parse и возвращает список документов
        :return:
        :rtype:
        """
        self.logger.debug("Parse process start")
        self._parse()
        self.logger.debug("Parse process finished")
        return self._content_document

    def _parse(self):
        """
        Метод, занимающийся парсингом. Он добавляет в _content_document документы, которые получилось обработать
        :return:
        :rtype:
        """
        # HOST - это главная ссылка на источник, по которому будет "бегать" парсер
        self.logger.debug(F"Parser enter to {self.HOST}")

        # ========================================
        # Тут должен находится блок кода, отвечающий за парсинг конкретного источника
        # -
        self.find_new_doc(self.HOST, 'Use of LED signal heads in road traffic signal systems', 'This Technical Specification considers only newly manufactured and installed signal controllers and signal heads for road traffic applications, using appropriate cabling. This Technical Specification considers only LED optical units with 200 mm and 300 mm roundels as standardised in EN 12368. It does not consider configurations such as an arrow or a pedestrian symbol, created by specifically positioned patterns of LEDs. This Technical Specification does not consider railway signalling applications.', datetime.datetime.strptime('2007-08-03', '%Y-%m-%d'))
        self.find_new_doc(self.HOST, 'Road traffic signal systems - Electromagnetic compatibility', 'This product standard for EMC requirements applies to road traffic signal systems. The range of products included within the scope of this European Standard are road traffic signal systems and devices including for example signal heads, signalling devices and traffic signs, controller and housing, supports, interconnections, traffic detectors, monitoring equipment, electrical supply. Road traffic signal systems operating in conjunction with other systems e.g. public lighting, railway systems should also comply with the respective standard and should not reduce the safety of all the equipment. Central Office equipment is excluded from this standard. Items with a radio-communication function should also refer to the European ETSI standards.', datetime.datetime.strptime('2012-06-29', '%Y-%m-%d'))
        self.find_new_doc(self.HOST, 'Road traffic signal systems', 'This document specifies requirements for Road Traffic Signal Systems, including their development, design, testing, installation and maintenance. In particular, it forms the electrotechnical part of the following two standards issued by CEN: - EN 12368, Traffic control equipment - Signal heads; - EN 12675, Traffic signal controllers - Functional safety requirements. Each of these standards above will be used with this standard either singly or together to define an operational equipment or system. This will be achieved by using the electrotechnical methods and testing defined in this standard. Where Road Traffic Signal Systems are to be used with other systems, e.g. public lighting or railway signalling and communication, this document will be used with any other respective standard(s) for the other associated systems to ensure that overall safety is not compromised. This document is applicable to traffic signal control equipment permanently and temporarily installed, and portable traffic control equipment, with the exception of portable traffic signal equipment only capable of controlling alternate / shuttle working lanes (as further defined in 3.2.10).', datetime.datetime.strptime('2018-09-28', '%Y-%m-%d'))

        # Логирование найденного документа
        # self.logger.info(self._find_document_text_for_logger(document))

        # ---
        # ========================================
        ...

    def find_new_doc(self, host: str, filename: str, abstract: str, date: datetime.datetime = datetime.datetime.now(), delay: float = 0.5):
        doc = SPP_document(None, filename, abstract, None, f'{host}/ugd/{filename}.pdf', None, {}, date, None)
        self._content_document.append(doc)
        self.logger.info(self._find_document_text_for_logger(doc))
        time.sleep(delay)

    @staticmethod
    def _find_document_text_for_logger(doc: SPP_document):
        """
        Единый для всех парсеров метод, который подготовит на основе SPP_document строку для логера
        :param doc: Документ, полученный парсером во время своей работы
        :type doc:
        :return: Строка для логера на основе документа
        :rtype:
        """
        return f"Find document | name: {doc.title} | link to web: {doc.web_link} | publication date: {doc.pub_date}"

    @staticmethod
    def some_necessary_method():
        """
        Если для парсинга нужен какой-то метод, то его нужно писать в классе.

        Например: конвертация дат и времени, конвертация версий документов и т. д.
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def nasty_download(driver, path: str, url: str) -> str:
        """
        Метод для "противных" источников. Для разных источника он может отличаться.
        Но основной его задачей является:
            доведение driver селениума до файла непосредственно.

            Например: пройти куки, ввод форм и т. п.

        Метод скачивает документ по пути, указанному в driver, и возвращает имя файла, который был сохранен
        :param driver: WebInstallDriver, должен быть с настроенным местом скачивания
        :_type driver: WebInstallDriver
        :param url:
        :_type url:
        :return:
        :rtype:
        """

        with driver:
            driver.set_page_load_timeout(40)
            driver.get(url=url)
            time.sleep(1)

            # ========================================
            # Тут должен находится блок кода, отвечающий за конкретный источник
            # -
            # ---
            # ========================================

            # Ожидание полной загрузки файла
            while not os.path.exists(path + '/' + url.split('/')[-1]):
                time.sleep(1)

            if os.path.isfile(path + '/' + url.split('/')[-1]):
                # filename
                return url.split('/')[-1]
            else:
                return ""
