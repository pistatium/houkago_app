#coding: utf-8


platforms = (
    (1, "Android"),
    (2, "iOS"),
    (9, "Web"),
)

def get_platform_id(plat_str):
  for p in platforms:
    if p[1].lower() == plat_str.lower():
      return p[0]
  return 0

show_status = (
    (1, "公開"),
    (0, "非公開")
)

# DBへのアクセスを減らすため、
# 途中変更の少ないカテゴリは直書きで運用する
# 順序の変更は不可
# カテゴリ追加の場合は一番下に追記する
# カテゴリ削除の場合は、カテゴリ名の先頭に｢#｣をつける

_cat_apps = (
  (10,"アプリ / ツール(日常的に使う)"),
  (10,"アプリ /ツール(あると便利)"),
  (10,"アプリ /カスタマイズ"),
  (10,"アプリ /情報収集"),
  (10,"アプリ /コミュニケーション"),
  (10,"アプリ /エンターテイメント"),
  (10,"アプリ /教育･学習"),
  (10,"アプリ /健康･医療"),
  (10,"アプリ /旅行･アウトドア"),
  (10,"アプリ /グルメ･フード"),
  (10,"アプリ /ビジネス"),
  (10,"アプリ /写真･動画"),
  (10,"アプリ /音楽"),
  (10,"アプリ /カスタマイズ"),
  (10,"ゲーム / 2Dアクション"),
  (10,"ゲーム / 3Dアクション"),
  (10,"ゲーム / "),
  (10,"ゲーム / アーケード"),
  (10,"ゲーム / 音楽"),
  (10,"ゲーム / シミュレーション"),
  (10,"ゲーム / ストラテジ"),
  (10,"ゲーム / カード･テーブル"),
  (10,"ゲーム / クイズ"),
  (10,"ゲーム / レースゲーム"),
)

_BASE_CID_GAME = 1000

class Category:
    def __init__(self, cid, label, group):
        self.id      = cid
        self.label   = label 
        self.group  = group # app, game

    def __repr__(self):
        return "[ %s Category.%d (%s) ]" % (self.group, self.id, self.label)

    @classmethod
    def getList(cls, group):
        group = group.capitalize()
        base_cid = 0 
        if group == 'App':
            cats = _cat_apps
        elif group == 'Game':
            cats = _cat_games
            base_cid = _BASE_CID_GAME
        else:
            return []
        categories = []
        for i,c in enumerate(cats):
            cid = base_cid + i
            if not c.startswith('#'):
              categories.append(Category(cid, c, group))
        return categories

    @classmethod
    def getById(cls, cid):
        category = ""
        categories = []
        if cid < _BASE_CID_GAME:
            if cid < len(_cat_apps):
                return Category(cid, _cat_apps[cid], 'App')
            else:
                return Category(cid, 'その他', 'App')
        else:
            cid = cid - _BASE_CID_GAME
            if cid < len(_cat_games):
                return Category(cid, _cat_games[cid], 'Game')
            else:
                return Category(cid, 'その他', 'Game')



def test():
    print repr(Category.getList('App'))
    print repr(Category.getList('Game'))
    print repr(Category.getList('Hoge'))
    print Category.getById(1001)
    print Category.getById(1200)

if __name__ == '__main__':
    test()