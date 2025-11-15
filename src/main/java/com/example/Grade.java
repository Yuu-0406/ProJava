public class Grade{
    public static void main(String[] args){
        printGrade(95);
        printGrade(63);
        printGrade(77);
    }

    static void printGrade(int point) {
        if (point >= 90){
            System.out.println("S");
        } else if (point >= 80) {
            System.out.println("A");
        } else if (point >= 70) {
            System.out.println("B");
        } else if (point >= 60) {
            System.out.println("C");
        } else{
            System.out.println("D");
        }
    }
}