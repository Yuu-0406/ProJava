public class SimpleFraction{
    int bunshi;
    int bunbo;

    //コンストラクタ
    SimpleFraction(int bunshi, int bunbo){
        this.bunshi = bunshi;
        this.bunbo = bunbo;
    }

    //インスタンスが表現している分数を
    //引数の整数を足し算した分数にするメソッド
    void add(int num){
        bunshi = bunshi + bunbo *num;
    }

    public static void main(String[] args){
        SimpleFraction frac1 = new SimpleFraction(2,3);
        SimpleFraction frac2 = new SimpleFraction(4,5);

        frac1.add(3);
        frac2.add(5);

        System.out.println(frac1.bunshi + "/" + frac1.bunbo);
        System.out.println(frac2.bunshi + "/" + frac2.bunbo);
    }
}
