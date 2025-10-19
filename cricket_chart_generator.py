import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image
import json
import os
import random

from matplotlib.lines import Line2D

class CricketChartGenerator:
    def __init__(self, output_dir="cricket_charts"):
        """Initialize chart generator with output directory"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style for professional look
        plt.style.use('dark_background')
        self.colors = {
            'primary': '#00A8E8',
            'secondary': '#F4D03F',
            'accent': '#E74C3C',
            'success': '#2ECC71',
            'background': '#1C1C1C'
        }
    
    def generate_run_rate_graph(self, match_data, filename="run_rate.png"):
        """Generate run rate comparison graph using match_data"""

        fig, ax = plt.subplots(figsize=(12, 6), facecolor=self.colors['background'])
        ax.set_facecolor('#2C2C2C')

        # Extract overs and cumulative runs from recent_overs
        recent_overs = match_data.get("recent_overs", [])
        overs = [over_data["over"] for over_data in recent_overs]
        runs = [over_data["runs"] for over_data in recent_overs]

        # Compute cumulative runs for current run rate calculation
        cumulative_runs = np.cumsum(runs).tolist()
        current_rr = [cumulative_runs[i] / overs[i] for i in range(len(overs))]

        # Required run rate (constant from JSON)
        required_rr = [match_data["run_rate"]["required"]] * len(overs)

        # Plot lines
        ax.plot(overs, current_rr, color=self.colors['primary'], 
                linewidth=3, label='Current Run Rate', marker='o', markersize=5)
        ax.plot(overs, required_rr, color=self.colors['accent'], 
                linewidth=2, linestyle='--', label='Required Run Rate')

        # Fill area between lines
        ax.fill_between(overs, current_rr, required_rr, 
                        where=(np.array(current_rr) >= np.array(required_rr)),
                        alpha=0.3, color=self.colors['success'], label='Ahead')
        ax.fill_between(overs, current_rr, required_rr,
                        where=(np.array(current_rr) < np.array(required_rr)),
                        alpha=0.3, color=self.colors['accent'], label='Behind')

        # Styling
        ax.set_xlabel('Overs', fontsize=14, fontweight='bold', color='white')
        ax.set_ylabel('Run Rate', fontsize=14, fontweight='bold', color='white')
        ax.set_title(
            f'Run Rate Comparison - {match_data["teams"]["batting"]} vs {match_data["teams"]["bowling"]}',
            fontsize=18, fontweight='bold', color='white', pad=20
        )
        ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
        ax.grid(True, alpha=0.2, linestyle='--')
        ax.tick_params(colors='white', labelsize=10)

        # Add current score annotation
        score = match_data['current_score']
        ax.text(0.98, 0.97, f"{score['runs']}/{score['wickets']} ({score['overs']} ov)",
                transform=ax.transAxes, fontsize=16, fontweight='bold',
                color=self.colors['secondary'], ha='right', va='top',
                bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, facecolor=self.colors['background'])
        plt.close()

        return filepath

    
    def generate_manhattan_chart(self, match_data, filename="manhattan.png"):
        """Generate Manhattan (runs per over) chart using match_data"""

        fig, ax = plt.subplots(figsize=(14, 6), facecolor=self.colors['background'])
        ax.set_facecolor('#2C2C2C')

        # Extract overs & runs from match_data
        recent_overs = match_data.get("recent_overs", [])
        overs = [over_data["over"] for over_data in recent_overs]
        runs_per_over = [over_data["runs"] for over_data in recent_overs]

        # Color code: green for good overs (10+), yellow for medium, red for low
        colors_list = []
        for runs in runs_per_over:
            if runs >= 10:
                colors_list.append(self.colors['success'])
            elif runs >= 7:
                colors_list.append(self.colors['secondary'])
            else:
                colors_list.append(self.colors['accent'])

        # Create bars
        bars = ax.bar(overs, runs_per_over, color=colors_list, 
                    edgecolor='white', linewidth=0.5, alpha=0.8)

        # Add value labels on bars
        for bar, runs in zip(bars, runs_per_over):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{runs}',
                ha='center', va='bottom', fontsize=9, 
                fontweight='bold', color='white')

        # Styling
        ax.set_xlabel('Overs', fontsize=14, fontweight='bold', color='white')
        ax.set_ylabel('Runs', fontsize=14, fontweight='bold', color='white')
        ax.set_title(
            f"Manhattan Chart - {match_data['teams']['batting']} vs {match_data['teams']['bowling']}",
            fontsize=18, fontweight='bold', color='white', pad=20
        )
        ax.set_xticks(overs)
        ax.tick_params(colors='white', labelsize=10)
        ax.grid(True, axis='y', alpha=0.2, linestyle='--')

        # Add average line
        if runs_per_over:  # avoid error on empty data
            avg_runs = np.mean(runs_per_over)
            ax.axhline(y=avg_runs, color=self.colors['primary'], 
                    linestyle='--', linewidth=2, label=f'Average: {avg_runs:.1f}')
            ax.legend(loc='upper right', fontsize=11, framealpha=0.9)

        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, facecolor=self.colors['background'])
        plt.close()

        return filepath

    
    def generate_wagon_wheel(self, match_data, filename="wagon_wheel.png"):
        fig, ax = plt.subplots(figsize=(10, 10), facecolor=self.colors['background'])
        ax.set_facecolor('#2C2C2C')
        
        field = patches.Circle((0, 0), 1, fill=False, edgecolor='white', linewidth=2)
        ax.add_patch(field)
        pitch = patches.Rectangle((-0.05, -0.2), 0.1, 0.4, fill=True, 
                                  facecolor='#8B7355', edgecolor='white', linewidth=1)
        ax.add_patch(pitch)

        # Extract from key moments
        shots = []
        for moment in match_data.get("key_moments", []):
            desc = moment.get("description", "").lower()
            runs = moment.get("runs", 0)

            angle = random.randint(0, 360)
            if "midwicket" in desc: angle = 135
            elif "covers" in desc: angle = 75
            elif "long-on" in desc: angle = 180
            elif "long-off" in desc: angle = 350
            elif "point" in desc: angle = 50
            elif "square leg" in desc: angle = 110

            distance = 0.7
            if runs == 6: distance = 0.95
            elif runs == 4: distance = 0.8

            shots.append((angle, distance, runs))

            if moment.get("type") == "wicket":
                shots.append((angle, 0.85, -1))  # mark wicket

        for angle, distance, runs in shots:
            x, y = distance*np.cos(np.radians(angle)), distance*np.sin(np.radians(angle))
            if runs == 6:
                color, marker, size = self.colors['accent'], '*', 200
            elif runs == 4:
                color, marker, size = self.colors['success'], 'o', 150
            elif runs == -1:
                color, marker, size = self.colors['secondary'], 'X', 180
            else:
                color, marker, size = self.colors['secondary'], 'o', 100

            ax.plot([0, x], [0, y], color=color, linewidth=2, alpha=0.6)
            ax.scatter(x, y, s=size, c=color, marker=marker, edgecolor='white', linewidth=1, zorder=5)

        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'Wagon Wheel - {match_data["teams"]["batting"]}', fontsize=18, fontweight='bold', color='white', pad=20)

        legend_elements = [
            Line2D([0], [0], marker='*', color='w', markerfacecolor=self.colors['accent'], markersize=12, label='Six', linestyle='None'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor=self.colors['success'], markersize=10, label='Four', linestyle='None'),
            Line2D([0], [0], marker='X', color='w', markerfacecolor=self.colors['secondary'], markersize=10, label='Wicket', linestyle='None'),
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)

        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, facecolor=self.colors['background'])
        plt.close()
        return filepath

    def generate_partnership_chart(self, match_data, filename="partnership.png"):
        fig, ax = plt.subplots(figsize=(12, 6), facecolor=self.colors['background'])
        ax.set_facecolor('#2C2C2C')

        partnership = match_data.get('partnerships', [])[0]
        if not partnership: return None

        runs = partnership["runs"]
        balls = partnership["balls"]

        ax.plot([0, balls], [0, runs], color=self.colors['primary'], linewidth=4, marker='o', markersize=8)
        ax.fill_between([0, balls], [0, runs], alpha=0.3, color=self.colors['primary'])

        ax.scatter(balls, runs, s=300, c=self.colors['secondary'], marker='*', edgecolor='white', linewidth=2, zorder=5)
        ax.annotate(f"{runs} runs in {balls} balls", (balls, runs), xytext=(10, 10), textcoords='offset points',
                    fontsize=11, fontweight='bold', color=self.colors['secondary'],
                    bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

        ax.set_xlabel('Balls', fontsize=14, fontweight='bold', color='white')
        ax.set_ylabel('Runs', fontsize=14, fontweight='bold', color='white')
        ax.set_title(f'Partnership Progression - {" & ".join(partnership["batsmen"])}', fontsize=18, fontweight='bold', color='white', pad=20)
        ax.grid(True, alpha=0.2, linestyle='--')
        ax.tick_params(colors='white', labelsize=10)

        plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, dpi=150, facecolor=self.colors['background'])
        plt.close()
        return filepath

    
    def generate_all_charts(self, match_data):
        """Generate all charts for the match"""
        
        charts = {}
        
        print("🎨 Generating charts...")
        
        charts['run_rate'] = self.generate_run_rate_graph(match_data)
        print(f"✅ Run Rate Graph: {charts['run_rate']}")
        
        charts['manhattan'] = self.generate_manhattan_chart(match_data)
        print(f"✅ Manhattan Chart: {charts['manhattan']}")
        
        charts['wagon_wheel'] = self.generate_wagon_wheel(match_data)
        print(f"✅ Wagon Wheel: {charts['wagon_wheel']}")
        
        charts['partnership'] = self.generate_partnership_chart(match_data)
        print(f"✅ Partnership Chart: {charts['partnership']}")
        
        return charts


# Usage Example
if __name__ == "__main__":
    # Load match data
    with open('commentary_script.json', 'r') as f:
        data = json.load(f)
    
    match_data = data['match_data']
    print("match data using ", match_data)
    
    print("=" * 60)
    print("CRICKET CHART GENERATOR")
    print("=" * 60)
    print()
    
    # Generate all charts
    chart_generator = CricketChartGenerator()
    charts = chart_generator.generate_all_charts(match_data)
    
    print("\n" + "=" * 60)
    print("✅ All charts generated successfully!")
    print(f"📁 Charts saved in: {chart_generator.output_dir}/")
    print("=" * 60)
    
    # Save chart paths for next step
    with open('chart_paths.json', 'w') as f:
        json.dump(charts, f, indent=2)