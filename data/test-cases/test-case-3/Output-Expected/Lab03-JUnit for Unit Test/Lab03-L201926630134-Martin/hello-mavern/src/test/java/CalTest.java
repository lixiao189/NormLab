/*import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class CalTest {
    @Test
    public void test() {
        Cal cal = new Cal();
        assertNotNull(cal);
    }

    @Test
    public void testAdd() {
        Cal cal = new Cal();
        assertEquals(3, cal.add(1, 2));
    }

    //This test can't run more than 1 second, else failed
    @Test(timeout = 1000)
    public void testTimeout() {
        Cal cal = new Cal();
        cal.squareRoot(3);
    }

    @Test(expected = ArithmeticException.class)
    public void testException() {
        Cal cal = new Cal();
        cal.divide(3, 0);
    }
}*/



/*import lec03.Cal;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

public class CalTest {
    @ParameterizedTest
    @CsvSource({"0,0,0", "1,1,2", "2, 3, 4", "3, 5, 8"})
    void parameterizedTest(int in1, int in2, int expected) {
        assertEquals(expected, new Cal().add(in1, in2));
    }
}*/