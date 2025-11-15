
public class Ex04{
    int jpn;
    int math;
    int eng;
    int sci;

    //インスタンスフィールドを初期化するコンストラクタ
    Ex04(int jpn, int math, int eng, int sci){
        this.jpn = jpn;
        this.math = math;
        this.eng = eng;
        this.sci = sci;
    }

    //sciの分も足すことに変更
    int score_sum() {
        return (jpn + math + eng + sci);
    }

    //すべてのインスタンスフィールドの値を
    //１行で出力するインスタンスメソッド
    void display(){
        System.out.println("(jon, math, eng, sci) = ("
        + jpn + ", " + math + ", " + eng + ", " + sci + ")");
    }

    public static void main(String[] args) {
        int total;
        Ex04 stdnt001 = new Ex04(67, 92, 75, 89);
        Ex04 stdnt002 = new Ex04(98, 54, 87, 66);

        total = stdnt001.score_sum() + stdnt002.score_sum();

        stdnt001.display();

        System.out.println(stdnt001.eng);
        System.out.println(total);
    }
}