public class CounterTest {
    public static void main(String[] args) {
        Counter counter   = new Counter();
        Counter counter2  = new CounterEx(3);

        CounterEx counterEx = new CounterEx(5);
        // CounterEx counterEx2 = new Counter();

        for (int i = 0; i < 10; i++) {
            counter.incl();
            counter2.incl();
            counterEx.incl();
        }

        //getCount()メソッド
        System.out.println("counter.getCount() = " + counter.getCount());
        System.out.println("counterEx.getCount() = " + counterEx.getCount());
        System.out.println("counter2.getCount() = " + counter2.getCount());

        //getLimit()メソッド
        //System.out.println("counter2.getLimit() = " + counter2.getLimit());
        System.out.println("counterEx.getLimit() = " + counterEx.getLimit());

            
        }


    }
