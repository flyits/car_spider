category_type_list = set()


class Types:
    ENERGY_TYPE = 1  # 动力类型
    ENGINE_TYPE = 2  # 发动机类型
    GEARBOX_TYPE = 3  # 变速箱类型
    CATEGORY_TYPE = 4  # 汽车类别
    MERCHANT_TYPE = 5  # 商户类型
    ARTICLE_TYPE = 6  # 文章类型
    AD_TYPE = 7  # 广告类型
    MODULE_TYPE = 8  # 汽车模块
    STANDARD_TYPE = 9  # 排放标准类型
    DISCOUNTS_TYPE = 10  # 优惠类型
    DRIVE_WAY_TYPE = 11  # 驱动方式类型

    typeList = {
        ENERGY_TYPE: {
            '汽油': 1,
            '新能源': 2,
            '纯电': 3,
            '柴油': 4,
            '插电混合': 5,
            '油电混合': 6,
            '增程式纯电动': 7,
            '天然气': 8,
            '其它': 9,
        },
        ENGINE_TYPE: {
            '涡轮增压': 10,
            '自然吸气': 11,
            '机械增压': 12,
            '双增压': 13,
            '其它': 14,
        },
        GEARBOX_TYPE: {
            '手自一体': 15,
            '单速变速箱': 16,
            '手动': 17,
            '双离合': 18,
            'CVT无级变速': 19,
            '机械自动': 20,
            '自动': 21,
            'E-CVT无级变速': 22,
            '序列式': 23,
            '其它': 24,
        },
        CATEGORY_TYPE: {
            '轿车': 25,
            '新能源': 26,
            'SUV': 27,
            'MPV': 28,
            '跑车': 29,
            '皮卡': 30,
            '微面': 31,
            '轻客': 32,
            '敞篷车': 33,
            '三厢': 34,
            '两厢': 35,
            '卡车': 36,
            '单厢': 37,
            '房车': 38,
            '客车': 39,
            '旅行车': 40,
            '跨界车': 41,
            '掀背车': 42,
            '其它': 43,
        },
        MERCHANT_TYPE: {
            '直营店': 44,
            '服务中心': 45,
            '代理人': 46,
            '销巴心选': 47,
            '商家': 48,
            '普通个人': 49,
            '个人门店': 50,
        },
        ARTICLE_TYPE: {
            '资讯': 51,
            '常见问题-卖车': 52,
            '常见问题-关于我们': 53,
        },
        AD_TYPE: {
            '首页': 54,
            '新车': 55,
            '二手车': 56,
            '租车': 57,
            '新能源': 58,
            '团购': 59,
        },
        MODULE_TYPE: {
            '新车': 60,
            '二手车': 61,
        },
        STANDARD_TYPE: {
            '国二': 62,
            '国三': 63,
            '国四': 64,
            '国五': 65,
            '国六': 66,
            '其它': 67,

            '欧五': 67,
        },
        DISCOUNTS_TYPE: {
            '全赠积分': 68,
            '消费补贴': 69,
        },
        DRIVE_WAY_TYPE: {
            '全时四驱': 70,
            '后轮驱动': 71,
            '前轮驱动': 72,
            '适时四驱': 73,
            '分时四驱': 74,
            '电动四驱': 75,
            '其它': 76,
        }
    }

    def getTypeId(self, version_item=None, name=None, value=None):

        if name == '车身型式' and value in self.typeList[self.CATEGORY_TYPE]:
            version_item['category_type_id'] = self.typeList[self.CATEGORY_TYPE][value]
        if name == '车型级别' and version_item['category_type_id'] == 0 and value.find('SUV') != -1 and value in \
                self.typeList[self.CATEGORY_TYPE]:
            version_item['category_type_id'] = self.typeList[self.CATEGORY_TYPE]['SUV']
        if name == '动力类型' and value in self.typeList[self.ENERGY_TYPE]:
            version_item['energy_type_id'] = self.typeList[self.ENERGY_TYPE][value]
        if name == '进气形式' and value in self.typeList[self.ENGINE_TYPE]:
            version_item['engine_type_id'] = self.typeList[self.ENGINE_TYPE][value]
        if name == '变速箱类型':
            value = value[value.find(' ') + 1:]
            if value in self.typeList[self.GEARBOX_TYPE]:
                version_item['gearbox_type_id'] = self.typeList[self.GEARBOX_TYPE][value]
        if name == '排气量' or name == '排量[mL]':
            version_item['displacements'] = value
        if name == '环保标准' and value in self.typeList[self.STANDARD_TYPE]:
            version_item['standard_type_id'] = self.typeList[self.STANDARD_TYPE][value]
        if name == '最大马力' or name == '最大马力[Ps]':
            version_item['horsepower'] = value
        if name == '驱动方式' or name == '驱动形式':
            if value.find('x') != -1:
                value = '后轮驱动'
            if value in self.typeList[self.DRIVE_WAY_TYPE]:
                version_item['drive_way_type_id'] = self.typeList[self.DRIVE_WAY_TYPE][value]
        if name == '厂商指导价':
            if value == '-':
                value = 0
            else:
                value = float(value[0:value.find('万')]) * 10000
            version_item['official_price'] = value
            version_item['xb_perk_price'] = value / 2
            version_item['return_points_price'] = value

        return version_item
