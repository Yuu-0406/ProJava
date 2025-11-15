class Tape{
    char[] cells = new char[5];
    int head = 0;

    void write(char data){
        cells[head] = data;
        head++;
    }

    char delete(){
        head--;
        return cells[head];
    }

    void view(){
        System.out.print("tape's state :");
        for (int i = 0; i < head; i++){
            System.out.print(" " + cells[i]);
        } 
        System.out.println();
    }
}

public class ReadWriteTest {
    public static void main(String[] args){
        Tape tape = new Tape();

        tape.write('5');
        tape.write('2');
        tape.write('+');

        tape.view();

        for (int i = 0; i < 5; i++){
            tape.delete();
        }
        tape.write('7');
    }
}