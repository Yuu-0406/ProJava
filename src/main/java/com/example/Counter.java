//スーパークラス（親クラス）
public class Counter{
    private int count;

    Counter(){
        count = 0;
    }

    //アクセサメソッド(accessor method)
    int getCount(){
        return count;
    }

    void incl(){
        count++;
    }
    void decl(){
        count--;
    }
    boolean isZero(){
        return (count == 0);
    }
}