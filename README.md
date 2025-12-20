# Optimizing Edge Gaming Slices through an Enhanced UPF and Analytics in Beyond-5G Networks (WPEIF 2025)

## Paper metadata
- **Title:** Optimizing Edge Gaming Slices through an Enhanced User Plane Function and Analytics in Beyond-5G Networks
- **Venue:** Anais do XVI Workshop de Pesquisa Experimental da Internet do Futuro (WPEIF)
- **Year:** 2025
- **DOI:** 10.5753/wpeif.2025.8714
- **URL:** https://sol.sbc.org.br/index.php/wpeif/article/view/35271
- **Authors:** Bruno Silva; Larissa Rodrigues Moreira; Flávio de Oliveira Silva; Rodrigo Moreira

---

## 1. Problem
Edge/cloud gaming is highly sensitive to latency and throughput. Even when MEC and slicing are available, the core network often lacks fine-grained, non-intrusive observability to estimate per-user/per-session latency and turn that into analytics that can inform control decisions.

This paper targets the gap of **estimating user-perceived latency passively inside the 5G core** and **closing the loop** by feeding the measurements into an analytics function to support more responsive slice/session management.

---

## 2. High-level idea
The paper proposes a closed loop across:
- **UPF (User Plane Function):** extended to produce passive latency estimates from live traffic on the **N3 interface**
- **NWDAF (Network Data Analytics Function):** consumes latency telemetry and applies analytics/ML (including game classification)
- **SMF (Session Management Function):** can be notified by NWDAF to support latency-aware operational decisions

In short:
1. The UPF becomes a passive latency sensor at the data plane.
2. NWDAF becomes the analytics brain (models + inference + reporting).
3. SMF is the control-plane endpoint that can react to NWDAF insights.

---

## 3. Contributions (as presented in the paper)
1. A UPF enhancement with a user-space monitoring/filtering pipeline to estimate latency per tunnel (TEID).
2. An experimental evaluation using a real dataset with gaming traffic features.
3. A comparative assessment of ML models for game classification (positioned as NWDAF analytics capability).

---

## 4. Architecture overview (conceptual)
**Core components:**
- 5G control plane functions (e.g., AMF/SMF/PCF/NRF/UDM/UDR/NSSF/NEF, etc.)
- **UPF** deployed in a Kubernetes environment (free5GC-based deployment)
- **NWDAF** as the analytics function receiving telemetry and producing insights

**Key link:**
- UPF exports per-TEID latency measurements to NWDAF.
- NWDAF can notify SMF regarding QoS degradation and analytics outcomes.

---

## 5. Method (main technical content)

### 5.1 Passive latency estimation at the UPF
The method monitors packets at the UPF without generating probe traffic (non-intrusive).

For a packet observed at the UPF:
- Let `t_in` be the observation time at ingress, and `t_out` the observation time at egress.
- The latency estimate is:
  
  **L = t_out - t_in**

For bidirectional exchanges (request + response), a total estimate can be expressed as:

- **L_total = (t_out^request - t_in^request) + (t_out^response - t_in^response)**

This time-shift approach enables continuous latency sampling from real traffic.

### 5.2 TEID-based per-user/session association
Because 5G user-plane traffic on N3 uses GTP-U tunnels, each session can be associated with a **TEID**.

Pipeline:
1. Capture traffic at the UPF on the **N3 interface**
2. Parse GTP-U headers and **extract TEID**
3. Maintain latency samples indexed by TEID, enabling per-session/per-UE analysis (and slice-scoped reasoning)

This turns “raw packet timing” into structured telemetry: **TEID → latency time series**.

### 5.3 NWDAF analytics and closed-loop feedback
Once the UPF produces per-TEID latency samples, NWDAF:
1. Ingests latency telemetry (optionally aggregating over windows)
2. Runs analytics/ML (including game classification)
3. Produces insights that can be used for QoS/QoE assessment
4. Notifies SMF to support corrective decisions (e.g., resource adjustments, policy updates, slice/session tuning)

Operational interpretation:
- UPF = sensor
- NWDAF = analyzer
- SMF = control-plane consumer of insights

---

## 6. ML models evaluated (NWDAF-side)
The paper evaluates multiple models for game classification:
- KNN
- Decision Tree (DT)
- Random Forest (RF)
- LSTM
- CatBoost

The goal is to demonstrate that NWDAF can host analytics capable of inferring application/game type and supporting QoS reasoning.

---

## 7. Experimental setup (reported)
- Infrastructure: VM-based environment (Fabric testbed)
- Platform: Kubernetes 1.28
- Core: free5GC-based deployment (including UPF modifications)
- Dataset: 69,395 instances with 16 features
- Classes: 3 game categories
  - League of Legends (LOL)
  - Teamfight Tactics (TFT)
  - Valorant (VAL)

---

## 8. Results summary (reported)

### 8.1 Passive latency estimation quality
The paper reports strong agreement between passive estimates and the baseline using normalized error metrics (and original MAPE), indicating that the passive approach can track latency with high fidelity.

### 8.2 Game classification performance
Tree-based methods are reported as top performers in the evaluated setting, with CatBoost and Random Forest achieving the best average performance over repeated runs, and high ROC/AUC behavior for CatBoost across classes.

---

## 9. Why it matters
- Passive measurement avoids probe overhead and reduces operational intrusion.
- TEID indexing matches 5G user-plane semantics, enabling per-session visibility.
- NWDAF integration enables analytics-driven, latency-aware insights that can inform control-plane actions for edge gaming slices.

---

## 10. BibTeX reference
```bibtex
@inproceedings{wpeif,
  author    = {Bruno Silva and Larissa Rodrigues Moreira and Fl{\'a}vio de Oliveira Silva and Rodrigo Moreira},
  title     = {Optimizing Edge Gaming Slices through an Enhanced User Plane Function and Analytics in Beyond-5G Networks},
  booktitle = {Anais do XVI Workshop de Pesquisa Experimental da Internet do Futuro},
  location  = {Natal/RN},
  year      = {2025},
  keywords  = {},
  issn      = {2595-2692},
  pages     = {1--8},
  publisher = {SBC},
  address   = {Porto Alegre, RS, Brasil},
  doi       = {10.5753/wpeif.2025.8714},
  url       = {https://sol.sbc.org.br/index.php/wpeif/article/view/35271}
}
