public class Calculator {
    public int add(int i, int j) {
        return i + j;
    }
    public int multiply(int i, int j) {
        return i * j;
    }

    public void squareRoot(int n) {
        for (; ; ) ;  // Bug : endless loop
    }

    public float divide(int i, int j) {
        return i / j;
    }
}
