# -*- coding: utf-8 -*-
import os

from storage import DataBuffer
from config import make_date

year, month, day = make_date()


class ItemPipeline:

    def open_spider(self, spider):
        # 初始化pipline
        city_name = spider.settings.get('city_name', '全国')
        clear_buffer = spider.settings.get('clear_buffer', False)
        self.save_name = spider.settings.get('save_name', '贝壳')
        self.save_dir = spider.settings.get('save_dir', 'data/')
        self.data = DataBuffer(name='_'.join([city_name, spider.name]), clear=clear_buffer)
        self.city_name = city_name

    def process_item(self, item, spider):
        # 缓存
        save_sheet = item.get('dtype') or self.save_name
        self.data[save_sheet].append(item.get('data') or item)
        return item

    def close_spider(self, spider):
        import traceback

        if not len(self.data):
            print('%s没有爬到数据，取消保存, 退出'% self.city_name)
            return

        # 存储
        # request_count = spider.crawler.stats.get_value('downloader/request_count', 0)
        # if request_count > 0:
        #     print("开始保存数据")
        #     try:
        #         file_prefix = os.path.join(self.save_dir, '{}_{}_'.format(f'{year}-{month}-{day}',
        #                                                                   self.city_name.encode('gbk').decode("gbk"), ))
        #         save_filepath = ''.join([file_prefix, '{}.xlsx'.format(self.save_name)])
        #         # 获取存储类型的设置
        #         save_format = spider.settings.get('save_format'.upper())
        #         fmt = {'excel': lambda: self.data.to_excel(save_filepath),
        #                'excel_div': lambda: self.data.to_excel_div(save_filepath, spider.settings.get('div_limit', 200000)),
        #                'csv': lambda: self.data.to_csv(file_prefix=file_prefix, format_data=True),
        #                'to_postgreSql': lambda: self.data.to_postgreSql()}
        #         save_method = fmt.get(save_format, fmt['to_postgreSql'])        # 直接保存到PostgreSql
        #         save_method()
        #
        #         # 保存一个空文件, 应对检查当选择不存入数据库时, 请注释此代码
        #         open(save_filepath,'w').close()
        #
        #     except BaseException as e:
        #         traceback.print_exc()
        #         print("%s,\n格式保存失败" % (e))
        # else:
        #     print('程序出错，取消保存')

