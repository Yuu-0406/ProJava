//サブクラス(子クラス)
public class CounterEx extends Counter{
    private int limit;

    CounterEx(int limit){
        super();  //スーパークラスのコンストラクタ呼び出し
        this.limit = (limit < 0 ) ? 0 : limit;
    }

    int getLimit(){
        return limit;
    }

    /*--- メソッドのオーバーライド ---*/
    @Override
    void incl(){
        if (getCount() < limit)
            super.incl();
    }

    @Override
    void decl(){
        if (super.getCount() > 0){
            super.decl();
        }
    }
}