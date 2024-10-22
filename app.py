from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# DataFrame to hold the budget data
budget_data = pd.DataFrame(columns=["Type", "Amount", "Category", "Date"])


@app.route('/')
def home():
    return render_template('index.html', data=budget_data.to_dict(orient='records'))


@app.route('/add', methods=['POST'])
def add_entry():
    global budget_data
    entry_type = request.form['type']
    amount = float(request.form['amount'])
    category = request.form['category']
    date = request.form['date']

    # Create a new DataFrame for the new entry
    new_entry = pd.DataFrame([{"Type": entry_type, "Amount": amount, "Category": category, "Date": date}])

    # Concatenate the new entry with the existing DataFrame
    budget_data = pd.concat([budget_data, new_entry], ignore_index=True)

    return redirect(url_for('home'))


@app.route('/visualize')
def visualize():
    if not budget_data.empty:
        fig, ax = plt.subplots()

        # Separate income and expenses
        income_data = budget_data[budget_data['Type'] == 'Income']
        expense_data = budget_data[budget_data['Type'] == 'Expense']

        # Plot trend lines
        ax.plot(income_data['Date'], income_data['Amount'].cumsum(), color='green', label='Income')
        ax.plot(expense_data['Date'], expense_data['Amount'].cumsum(), color='red', label='Expenses')

        ax.set_title('Spending and Income Trend')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Amount')
        ax.legend()

        # Save the figure
        fig.savefig('static/visualization.png')
        plt.close(fig)

        return render_template('visualize.html')
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
