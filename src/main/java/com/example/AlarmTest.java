public class AlarmTest{
    public static void main(String[] args) {
        CountUpAlarm alarm = new CountUpAlarm(5);

        for (int i = 0; i < 10; i++) {
            alarm.countUp();
            //alarm.counter.incl(); NG    
        }
            
        
    }
}