//Counterクラスの派生クラス
public class CountUpAlarm{
    private Counter counter;
    private int max;

    CountUpAlarm(int max){
        counter = new Counter();
        this.max = max;
    }

    void countUp(){
        if (counter.getCount() >= max)
            return;

        counter.incl();
        System.out.println(counter.getCount());
        if (counter.getCount() == max){
            System.out.println("最大値に到達!");
        }
    }
}