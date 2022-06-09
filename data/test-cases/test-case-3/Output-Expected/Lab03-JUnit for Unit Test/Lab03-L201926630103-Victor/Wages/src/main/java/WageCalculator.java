public class WageCalculator {
    // standardHrs = s, holidayHrs = h
    public int compensation(int s, int h) {
        int wages = 0;

        if(s==40 && h==0) {
            wages = s*20;
        }
        else if(s==40 && h>0) {
            wages  = s*20 + h*40;
        }
        else if (s>40 && h==0) {
            s = s % 40;
            wages = 40*20 + s*30;
        }
        else if (s>40 && h>0) {
            s = s % 40;
            wages = 40*20 + s*30 + h*40;
        }
        else if (s==0 && h==0) {
            wages = 0;
        }
        else if (s==0 && h>0) {
            wages =  h*40;
        }
        else
            wages = 0;

    return wages;
    }

    public float divide(int i, int j) {
        return i / j;
    }

    public void squareRoot(int n) {
        for (; ; ) ;    // Bug : endless loop
    }
}
