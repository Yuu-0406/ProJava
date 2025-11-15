public class Horse extends Animal{

    //引数なしコンストラクタ
    Horse(){
        super("horse");
    }

    //文字列を引数としてとるコンストラクタ
    Horse(String name){
        super(name);
    }

    //抽象メソッドをオーバーライド
    @Override
    public void naku(){
        System.out.println("ヒヒ―ン");
    }

    //確認用コード
    public static void main(String[] args) {
        Animal horse = new Horse();
        Animal goldship = new Horse("Gold Ship");
        
        System.out.print(horse.getName() + "の鳴き声:");
        horse.naku();

        System.out.print(goldship.getName() + "の鳴き声:");
        goldship.naku();

    }
}