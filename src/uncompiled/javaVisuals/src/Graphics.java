import javax.swing.JPanel;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.renderer.xy.XYBarRenderer;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.util.ArrayList;

import javax.swing.*;
import javax.swing.table.*;

import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.event.*;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.RangeType;
import org.jfree.data.xy.IntervalXYDataset;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import org.jfree.ui.*;

//Model of the table
class DemoTableModel extends AbstractTableModel implements TableModel {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	private Object data[][];

	public int getColumnCount() {
		return 2;
	}

	public int getRowCount() {
		return data.length;
	}

	public Object getValueAt(int i, int j) {
		return data[i][j];
	}

	public void setValueAt(Object obj, int i, int j) {
		data[i][j] = obj;
		fireTableDataChanged();
	}

	public String getColumnName(int i) {
		switch (i) {
		case 0: // '\0'
			return "Gene:";

		case 1: // '\001'
			return "Number of hits:";

		}
		return null;
	}

	public DemoTableModel(int i) {
		data = new Object[i][2];
	}
}

// Class to create a graphic
class Graphics extends ApplicationFrame implements ChartChangeListener,
		ChartProgressListener {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	JComboBox jComboBox1;
	private ChartPanel chartPanel;
	private DemoTableModel model;
	XYSeriesCollection dataSet;
	ArrayList<Species> speciesList; // List with all species
	int currentSpecies; // set the species (by index number) used in the current
						// visualization

	public Graphics(ArrayList<Species> speciesList) {
		super("VirusLand");
		this.speciesList = speciesList;
		this.currentSpecies = 0;

		/* Starts build upper box */
		JPanel jpanel2 = new JPanel(null);
		jpanel2.setPreferredSize(new Dimension(300, 100));
		jpanel2.setBorder(BorderFactory.createEmptyBorder(0, 4, 4, 4));
		this.jComboBox1 = new javax.swing.JComboBox();
		JLabel jLabel1 = new javax.swing.JLabel();
		JButton jButton1 = new javax.swing.JButton();
		jButton1.addActionListener(new java.awt.event.ActionListener() {
			public void actionPerformed(java.awt.event.ActionEvent evt) {
				clickButton(evt);
			}
		});

		jComboBox1.setModel(new javax.swing.DefaultComboBoxModel(
				generateListOfSpeciesName()));
		jpanel2.add(jComboBox1);
		jComboBox1.setBounds(10, 50, 420, 30);
		jLabel1.setFont(new java.awt.Font("Tahoma", 0, 12)); // NOI18N
		jLabel1.setText("Select the species you want to visualize:");
		getContentPane().add(jLabel1);
		jLabel1.setBounds(10, 10, 279, 36);
		jButton1.setText("Generate");
		jpanel2.add(jButton1);
		jButton1.setBounds(440, 50, 85, 30);

		/* Finish upper box */
		// Creating plot panel
		this.setLayout(new BorderLayout());
		JPanel panel = new JPanel(new BorderLayout());
		JFreeChart jfreechart = createChart(this.currentSpecies);
		chartPanel = new ChartPanel(jfreechart);
		chartPanel.setPreferredSize(new Dimension(600, 270));
		chartPanel.setDomainZoomable(true);
		chartPanel.setRangeZoomable(true);
		javax.swing.border.CompoundBorder compoundborder = BorderFactory
				.createCompoundBorder(
						BorderFactory.createEmptyBorder(4, 4, 4, 4),
						BorderFactory.createEtchedBorder());
		chartPanel.setBorder(compoundborder);
		panel.add(new JScrollPane(chartPanel));
		// ends plot panel

		// building table
		JPanel jpanel1 = new JPanel(new BorderLayout());
		jpanel1.setPreferredSize(new Dimension(400, 120));
		jpanel1.setBorder(BorderFactory.createEmptyBorder(0, 4, 4, 4));

		model = new DemoTableModel(1);
		model.setValueAt("", 0, 0);
		model.setValueAt("", 0, 1);

		JTable jtable = new JTable(model);
		jpanel1.add(new JScrollPane(jtable));
		panel.add(jpanel1, "South");
		panel.add(jpanel2, "North");
		add(panel);
		// finishing table
		this.pack();
		RefineryUtilities.centerFrameOnScreen(this);
		this.setVisible(true);
	}

	private Object[] generateListOfSpeciesName() {
		String[] listOfSpeciesName = new String[this.speciesList.size()];
		for (int i = 0; i < this.speciesList.size(); i++) {
			listOfSpeciesName[i] = this.speciesList.get(i).name;
		}
		return listOfSpeciesName;
	}

	// structure to create a chart
	private JFreeChart createChart(int currentSpecies) {

		Species species = this.speciesList.get(currentSpecies);
		IntervalXYDataset dataset = createDataset(species);
		JFreeChart jfreechart = ChartFactory.createXYBarChart(
				"" + species.getName() + "   " + species.getAccessionNumber(),
				"Genes", false, "# of Hits", dataset, PlotOrientation.VERTICAL,
				true, false, false);
		jfreechart.setBackgroundPaint(Color.white);
		XYPlot xyplot = (XYPlot) jfreechart.getPlot();
		xyplot.setBackgroundPaint(Color.lightGray);
		xyplot.setDomainGridlinePaint(Color.white);
		xyplot.setRangeGridlinePaint(Color.white);
		xyplot.setOrientation(PlotOrientation.VERTICAL);
		xyplot.setBackgroundPaint(Color.lightGray);
		xyplot.setDomainGridlinePaint(Color.white);
		xyplot.setRangeGridlinePaint(Color.white);
		xyplot.setAxisOffset(new RectangleInsets(5D, 5D, 5D, 5D));
		xyplot.setDomainCrosshairVisible(true);
		xyplot.setDomainCrosshairLockedOnData(false);
		xyplot.setRangeCrosshairVisible(false);
		NumberAxis numberaxis = (NumberAxis) xyplot.getDomainAxis();
		numberaxis.setStandardTickUnits(NumberAxis.createIntegerTickUnits());
		numberaxis.setRangeType(RangeType.POSITIVE);
		xyplot.setRenderer(new XYBarRenderer(.5));
		XYBarRenderer xybarrenderer = (XYBarRenderer) xyplot.getRenderer();
		xybarrenderer.setDrawBarOutline(false);
		jfreechart.addChangeListener(this);
		jfreechart.addProgressListener(this);
		jfreechart.setBackgroundPaint(Color.white);
		return jfreechart;
	}

	// Action to the button to generate a new Graphics
	private void clickButton(ActionEvent evt) {
		generateNewGraphic();
	}

	private void generateNewGraphic() {
		this.currentSpecies = this.jComboBox1.getSelectedIndex();
		this.chartPanel.setChart(createChart(this.currentSpecies));
		this.chartPanel.repaint();
		this.repaint();

	}

	private IntervalXYDataset createDataset(Species species) {
		XYSeries xyseries = new XYSeries("Number of Hits");
		for (int i = 0; i < species.getTotalNumberOfProteins(); i++) {
			xyseries.add(i, species.proteinList.get(i).numberOfHits);// get the
																		// number
																		// of
																		// hits
																		// by
																		// protein

		}
		XYSeriesCollection xyseriescollection = new XYSeriesCollection();
		xyseriescollection.addSeries(xyseries);
		this.dataSet = xyseriescollection;
		return xyseriescollection;
	}

	public void chartChanged(ChartChangeEvent chartchangeevent) {
		if (chartPanel != null) {
			JFreeChart jfreechart = chartPanel.getChart();
			if (jfreechart != null) {

				XYPlot xyplot = (XYPlot) jfreechart.getPlot();
				double d = xyplot.getDomainCrosshairValue();
				d = Math.round(d);
				if (((int) d) < this.speciesList.get(currentSpecies)
						.getTotalNumberOfProteins()) {
					Double y = this.dataSet.getYValue(0, (int) d);

					// get the accession number of the protein in the protein
					// list,
					// at the posicion of the line crossing in the plot,in the
					// current Specie
					// in the list of Species
					model.setValueAt(
							this.speciesList.get(this.currentSpecies).proteinList
									.get((int) d).accessionNumber, 0, 0);
					model.setValueAt(y, 0, 1);
				}
			}

		}

	}

	public void chartProgress(ChartProgressEvent chartprogressevent) {
		if (chartprogressevent.getType() != 2)
			return;
		if (chartPanel != null) {
			JFreeChart jfreechart = chartPanel.getChart();
			if (jfreechart != null) {
				XYPlot xyplot = (XYPlot) jfreechart.getPlot();
				double d = xyplot.getDomainCrosshairValue();
				d = Math.round(d);
				if (((int) d) < this.speciesList.get(currentSpecies)
						.getTotalNumberOfProteins()) {
					Double y = this.dataSet.getYValue(0, (int) d);

					// get the accession number of the protein in the protein
					// list,
					// at the posicion of the line crossing in the plot,in the
					// current Specie
					// in the list of Species
					model.setValueAt(
							this.speciesList.get(this.currentSpecies).proteinList
									.get((int) d).accessionNumber, 0, 0);
					model.setValueAt(y, 0, 1);
				}

			}
		}
	}

	/**
	 * Starting point for the demonstration application.
	 * 
	 * @param args
	 *            ignored.
	 */
	public static void main(String[] args) {

		FrameSequence f = new FrameSequence();

	}

}
