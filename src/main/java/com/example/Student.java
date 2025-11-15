public class Student{
    int jpn;
    int math;
    int eng;

    int score_sum() {
        return (jpn + math + eng);
    }

    public static void main(String[] args) {
        int total;
        Student stdnt001 = new Student();
        Student stdnt002 = new Student();

        stdnt001.jpn = 67;
        stdnt001.math = 92;
        stdnt001.eng = 75;

        stdnt002.jpn = 98;
        stdnt002.math = 54;
        stdnt002.eng = 87;

        total = stdnt001.score_sum() + stdnt002.score_sum();

        System.out.println(stdnt001.eng);
        System.out.println(total);
    }
}