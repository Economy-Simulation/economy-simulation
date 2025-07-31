# 🌍 Economy Simulation

*The most comprehensive, high-performance, and modular simulation of the real-world global economy*

---

## 🌍 Vision

> **To create the most comprehensive, high-performance, and modular simulation of the real-world global economy — empowering individuals, companies, and institutions to understand, explore, and forecast the complex interdependencies of our planetary markets.**

**Key Pillars:**
- **🌐 Global Scale:** Simulate 190+ nations, markets, currencies, and production chains with adjustable granularity
- **👥 Universal Access:** Built for corporate strategists, investors, researchers, governments, and developers
- **🔧 Open & Modular:** Fully open-source with extensible APIs for infinite customization
- **🚀 Future-Ready:** Supporting historical reconstructions and real-time integrations

---

## 🏗️ Project Structure

```
economy-simulation/
├── backend/
│   └── global-economy-sim/    # Core Python simulation engine
├── frontend/                  # Web-based interface and visualization
├── pyproject.toml            # Hatch project configuration
├── LICENSE                   # MIT License
└── README.md                 # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Hatch](https://hatch.pypa.io/) for Python environment management

### Development Setup

1. **Install Hatch** (if not already installed):
   ```bash
   pip install hatch
   ```

2. **Clone the repository**:
   ```bash
   git clone https://github.com/filip-herceg/economy-simulation.git
   cd economy-simulation
   ```

3. **Set up development environment**:
   ```bash
   hatch env create
   ```

4. **Activate the environment**:
   ```bash
   hatch shell
   ```

### Available Commands

- **Run tests**: `hatch run test` *(coming soon)*
- **Build package**: `hatch build`
- **Install in development mode**: `hatch run pip install -e .`

*Note: Development is in early stages - more commands and features coming soon*

---

## 🤖 Smart Auto-Versioning

This project uses an AI-powered smart versioning system that automatically:
- **Analyzes code changes** using semantic analysis
- **Determines version bumps** (MAJOR/MINOR/PATCH) based on impact
- **Creates releases** with automated changelogs
- **Maintains semantic versioning** without manual intervention

### For Contributors
- Just push your changes to main
- The system automatically analyzes your code changes
- Version bumps and releases happen automatically
- No need to manually update version numbers

### Setup (Maintainers Only)
See `SECURE-VERSIONING-SETUP.md` for GitHub App setup instructions.

---

## 🤝 Contributing

This is an ambitious open-source project that welcomes contributors from all backgrounds - economists, developers, data scientists, and domain experts. Help us build the future of economic simulation.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).