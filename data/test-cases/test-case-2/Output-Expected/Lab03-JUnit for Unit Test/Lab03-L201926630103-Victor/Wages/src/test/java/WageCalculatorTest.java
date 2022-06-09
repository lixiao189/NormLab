import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

public class WageCalculatorTest {
    WageCalculator wc;

    @Before
    public void test() {
        wc = new WageCalculator();
        assertNotNull(wc);
    }

    @Test
    public void testCompensation() throws Exception {
        int result = new WageCalculator().compensation(40, 0);
        assertEquals(800, result);
    }

    @Test
    public void withStdHoursAndHolidayHours() {
        assertEquals(950, new WageCalculator().compensation(45,0));
        assertEquals(1040, new WageCalculator().compensation(48,0));
    }

    @Test
    public void withStdHoursAndWithoutHolidayHours() {
        assertEquals(920, new WageCalculator().compensation(40,3));
        assertEquals(1030, new WageCalculator().compensation(45,2));
        assertEquals(1280, new WageCalculator().compensation(48,8));
    }

    @Test
    public void withoutStdHoursAndWithHolidayHours() {
        assertEquals(120, new WageCalculator().compensation(0,3));
        assertEquals(80, new WageCalculator().compensation(0,2));
    }

    @Test
    public void withoutStdHoursAndWithoutHolidayHours() {
        assertEquals(0, new WageCalculator().compensation(0,0));
    }

    @Test(expected = ArithmeticException.class)
    public void testException() {
        wc.divide(3, 0);
    }

    //This test can't run more than 1 second, else failed
    @Test(timeout = 1000)
    public void testTimeout() {
        wc.squareRoot(3);
    }
}
