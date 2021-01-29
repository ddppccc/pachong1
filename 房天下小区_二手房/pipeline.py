import os
from datetime import datetime
from storage import DataBuffer
from hashlib import md5
from scrapy.exceptions import DropItem
import xlrd


class ItemPipeline:

    def open_spider(self, spider):
        # 初始化pipline参数
        city_name = spider.settings.get('city_name', '全国')
        clear_buffer = spider.settings.get('clear_buffer', False)
        self.save_name = spider.settings.get('save_name', '安居客')
        self.save_dir = spider.settings.get('save_dir', 'data1/')
        self.data = DataBuffer(name='_'.join([city_name, spider.name]), clear=clear_buffer)
        self.city_name = city_name
        # 初始化去重
        self.duplicate_field = spider.settings.get("duplicate_field".upper())

    def process_item(self, item, spider):
        # 缓存
        save_sheet = item.get('dtype') or self.save_name
        
        # 去重, 目前仅支持单表存储的数据类型
        self.duplicate(item, table_name=save_sheet, spider=spider)
        
        # 添加数据至缓存
        self.data[save_sheet].append(item.get('data1') or item)
        
        return item

    def close_spider(self, spider):
        import traceback

        # 确定爬虫是否正常运行
        if not len(self.data):
            print('%s没有爬到数据，取消保存, 退出'% self.city_name)
            with open('data1/%s缺失.txt'%self.city_name,'w') as f:
                pass
            return

        request_count = spider.crawler.stats.get_value('downloader/request_count', 0)
        if request_count > 0:
            print("开始保存数据")
        else:
            print('程序出错，取消保存')
            return

        # 保存数据
        # 配置参数
        # 文件名前缀
        file_prefix = os.path.join(self.save_dir,
                                   '{}_{}_'.format(datetime.now().strftime('%y-%m-%d'), self.city_name, ))
        # 拼接excel文件名
        save_filepath = ''.join([file_prefix, '{}.xlsx'.format(self.save_name)])

        # 获取存储类型的设置
        save_format = spider.settings.get('save_format'.upper())
        print(save_format,"=========================================")


        # 失败存储方案
        fail_fmt = spider.settings.get("save_format2".upper())

        # 分段存储长度
        div_limit = spider.settings.get('div_limit'.upper(), 200000)

        # 存储函数字典
        fmt = {'excel': lambda: self.data.to_excel(save_filepath),
               'excel_div': lambda: self.data.to_excel_div(save_filepath, div_limit),
               'csv': lambda: self.data.to_csv(file_prefix=file_prefix, format_data=True), }

        # 获取对应的存储函数
        save_method = fmt.get(save_format, fmt['excel'])

        # 尝试存储
        try:
            save_method()
            print(save_filepath)
        except BaseException as e:
            traceback.print_exc()
            print("%s,\n%s格式保存失败" % (e, save_format))


            # 采取方案二
            if fail_fmt:
                # 获取对应的存储函数
                save_method = fmt.get(save_format, fmt['excel'])
                print("尝试存储方案2:%s", save_method)
                try:
                    save_method()
                    print(save_filepath)
                except BaseException as e:
                    traceback.print_exc()
                    print("%s,\n%s格式保存失败" % (e, save_format))

    def duplicate(self, item, table_name, spider):
        """
        去重,设置DUPLICATE_FIELD参数为去重字段即可
        :param item:
        :param table_name:
        :return:
        """
        dname = 'duplicate_' + table_name
        if self.duplicate_field and not hasattr(self, dname):
            if self.data.existed:   # 如果有历史数据,从历史数据中加载去重字段
                print("从数据库中加载去重字段")
                duplicated_set = set([self.make_dup_code(i[self.duplicate_field]) for i in self.data.db.select2dict(table_name, fields=(self.duplicate_field, ))])
            else:
                duplicated_set = set()
                print("新建一个去重集合")
            setattr(self, dname, duplicated_set)
            setattr(spider, dname, duplicated_set)
        elif self.duplicate_field:
            duplicated_set = getattr(self, dname)
            # 已存在数据去重
            dup_code = self.make_dup_code(item[self.duplicate_field])
            if self.duplicate_field and dup_code not in duplicated_set:
                duplicated_set.add(dup_code)
            else:
                raise DropItem

    @staticmethod
    def make_dup_code(x):
        return md5(str(x).encode()).hexdigest()



"""
{'downloader/request_bytes': 250371,
 'downloader/request_count': 424,
 'downloader/request_method_count/GET': 424,
 'downloader/response_bytes': 4880341,
 'downloader/response_count': 424,
 'downloader/response_status_count/200': 212,
 'downloader/response_status_count/301': 212,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2018, 10, 16, 4, 3, 27, 836020),
 'item_scraped_count': 5900,
 'log_count/INFO': 10,
 'request_depth_max': 1,
 'response_received_count': 212,
 'scheduler/dequeued': 424,
 'scheduler/dequeued/memory': 424,
 'scheduler/enqueued': 424,
 'scheduler/enqueued/memory': 424,
 'start_time': datetime.datetime(2018, 10, 16, 4, 0, 2, 494778)}"""