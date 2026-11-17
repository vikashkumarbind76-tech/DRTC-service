admin_html = '''{% extends "admin/base_site.html" %}
{% load i18n static log %}

{% block extrastyle %}
{{ block.super }}
<style>
  /* ==========================================================================
     EXACT REPLICA ADMIN DASHBOARD (MOCKUP BOTTOM-RIGHT)
     ========================================================================== */
  .admin-layout-wrap {
    display: flex;
    gap: 1.5rem;
    min-height: calc(100vh - 120px);
    width: 100%;
    max-width: 100%;
    box-sizing: border-box;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  }

  /* Left Sidebar */
  .admin-sidebar {
    width: 240px;
    background: #060e18;
    border: 1px solid rgba(0, 240, 255, 0.15);
    border-radius: 16px;
    padding: 1.5rem 1rem;
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  }

  @media (max-width: 900px) {
    .admin-layout-wrap {
      flex-direction: column;
    }
    .admin-sidebar {
      width: 100%;
    }
  }

  .sidebar-brand-box {
    padding-bottom: 1.25rem;
    margin-bottom: 1.25rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .sidebar-brand-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.5px;
    line-height: 1.1;
  }

  .sidebar-brand-sub {
    font-size: 0.68rem;
    font-weight: 700;
    color: #00d2d3;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px;
    display: block;
  }

  .sidebar-nav-list {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    list-style: none;
    margin: 0;
    padding: 0;
  }

  .sidebar-nav-item a {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.65rem 0.95rem;
    color: #94a3b8;
    font-size: 0.86rem;
    font-weight: 600;
    border-radius: 10px;
    text-decoration: none;
    transition: all 0.2s ease;
  }

  .sidebar-nav-item a:hover {
    color: #ffffff;
    background: rgba(0, 240, 255, 0.08);
  }

  .sidebar-nav-item.active a {
    color: #030a10;
    background: linear-gradient(135deg, #00d2d3, #00f0ff);
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(0, 210, 255, 0.35);
  }

  /* Main Dashboard Body */
  .admin-main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    min-width: 0;
  }

  /* Header Row */
  .dash-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    background: #060e18;
    border: 1px solid rgba(0, 240, 255, 0.15);
    border-radius: 16px;
    padding: 1.25rem 1.75rem;
  }

  .dash-title-main {
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin: 0;
  }

  .dash-sub-main {
    font-size: 0.84rem;
    color: #94a3b8;
    margin-top: 3px;
  }

  .dash-filter-select {
    background: rgba(8, 24, 38, 0.85);
    border: 1px solid rgba(0, 240, 255, 0.25);
    color: #ffffff;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-size: 0.84rem;
    font-weight: 600;
    cursor: pointer;
    outline: none;
  }

  /* 4 Stat Cards Grid */
  .dash-stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.25rem;
  }

  @media (max-width: 1024px) {
    .dash-stats-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 500px) {
    .dash-stats-grid {
      grid-template-columns: 1fr;
    }
  }

  .dash-stat-card {
    background: #060e18;
    border: 1px solid rgba(0, 240, 255, 0.15);
    border-radius: 16px;
    padding: 1.35rem 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    transition: transform 0.2s ease, border-color 0.2s ease;
  }

  .dash-stat-card:hover {
    transform: translateY(-3px);
    border-color: rgba(0, 240, 255, 0.4);
  }

  .dash-stat-top {
    display: flex;
    align-items: center;
    gap: 0.65rem;
  }

  .dash-stat-icon {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
  }

  .dash-stat-icon.cyan {
    background: rgba(0, 240, 255, 0.12);
    color: #00f0ff;
    border: 1px solid rgba(0, 240, 255, 0.3);
  }

  .dash-stat-icon.orange {
    background: rgba(245, 158, 11, 0.12);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.3);
  }

  .dash-stat-icon.green {
    background: rgba(16, 185, 129, 0.12);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
  }

  .dash-stat-icon.teal {
    background: rgba(20, 184, 166, 0.12);
    color: #2dd4bf;
    border: 1px solid rgba(20, 184, 166, 0.3);
  }

  .dash-stat-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #94a3b8;
  }

  .dash-stat-val {
    font-size: 1.85rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    margin-top: 0.25rem;
  }

  /* Recent Bookings Table Box */
  .dash-table-box {
    background: #060e18;
    border: 1px solid rgba(0, 240, 255, 0.15);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  }

  .dash-table-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.25rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .dash-table-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #ffffff;
  }

  .dash-view-all-link {
    font-size: 0.82rem;
    font-weight: 700;
    color: #00d2d3;
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .dash-view-all-link:hover {
    color: #00f0ff;
    text-decoration: underline;
  }

  .dash-table-wrap {
    overflow-x: auto;
  }

  .clean-dash-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
  }

  .clean-dash-table th {
    font-size: 0.75rem;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }

  .clean-dash-table td {
    padding: 0.95rem 1rem;
    font-size: 0.86rem;
    color: #cbd5e1;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  }

  .clean-dash-table tr:hover td {
    background: rgba(0, 240, 255, 0.03);
  }

  .badge-status-pill {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
  }

  .badge-status-pill.confirmed {
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
  }

  .badge-status-pill.pending {
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.35);
  }

  .badge-status-pill.completed {
    background: rgba(0, 240, 255, 0.15);
    color: #22d3ee;
    border: 1px solid rgba(0, 240, 255, 0.35);
  }
</style>
{% endblock %}

{% block coltype %}colM{% endblock %}
{% block bodyclass %}{{ block.super }} dashboard{% endblock %}
{% block breadcrumbs %}{% endblock %}
{% block content_title %}{% endblock %}

{% block content %}
<div class="admin-layout-wrap">
  <!-- Left Sidebar (Exact from Mockup) -->
  <aside class="admin-sidebar">
    <div class="sidebar-brand-box">
      <div class="sidebar-brand-title">DRTC SERVICE</div>
      <span class="sidebar-brand-sub">ADMIN DASHBOARD</span>
    </div>

    <ul class="sidebar-nav-list">
      <li class="sidebar-nav-item active">
        <a href="{% url 'admin:index' %}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
          <span>Dashboard</span>
        </a>
      </li>
      <li class="sidebar-nav-item">
        <a href="{% url 'admin:drtc_app_booking_changelist' %}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
          <span>Bookings</span>
        </a>
      </li>
      <li class="sidebar-nav-item">
        <a href="{% url 'admin:auth_user_changelist' %}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          <span>Customers</span>
        </a>
      </li>
      <li class="sidebar-nav-item">
        <a href="{% url 'admin:drtc_app_servicepackage_changelist' %}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
          <span>Pricing</span>
        </a>
      </li>
      <li class="sidebar-nav-item">
        <a href="{% url 'admin:drtc_app_customerreview_changelist' %}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
          <span>Gallery</span>
        </a>
      </li>
      <li class="sidebar-nav-item">
        <a href="{% url 'admin:drtc_app_contactinquiry_changelist' %}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
          <span>Enquiries</span>
        </a>
      </li>
      <li class="sidebar-nav-item">
        <a href="{% url 'admin:auth_user_changelist' %}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
          <span>Users</span>
        </a>
      </li>
      <li class="sidebar-nav-item">
        <a href="{% url 'admin:index' %}">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
          <span>Settings</span>
        </a>
      </li>
    </ul>
  </aside>

  <!-- Main Dashboard View -->
  <main class="admin-main-content">
    <!-- Header -->
    <div class="dash-header-row">
      <div>
        <h1 class="dash-title-main">Dashboard</h1>
        <div class="dash-sub-main">Overview of your tank cleaning service.</div>
      </div>
      <div>
        <select class="dash-filter-select">
          <option selected>Last 30 Days</option>
          <option>Today</option>
          <option>This Week</option>
          <option>This Year</option>
        </select>
      </div>
    </div>

    <!-- 4 Stat Cards Grid (Exact from Mockup) -->
    <div class="dash-stats-grid">
      <!-- 1. Total Bookings -->
      <div class="dash-stat-card">
        <div class="dash-stat-top">
          <div class="dash-stat-icon cyan">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
          </div>
          <span class="dash-stat-label">Total Bookings</span>
        </div>
        <div class="dash-stat-val">{{ kpi.total_bookings|default:"128" }}</div>
      </div>

      <!-- 2. Pending -->
      <div class="dash-stat-card">
        <div class="dash-stat-top">
          <div class="dash-stat-icon orange">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
          </div>
          <span class="dash-stat-label">Pending</span>
        </div>
        <div class="dash-stat-val">{{ kpi.pending_bookings|default:"24" }}</div>
      </div>

      <!-- 3. Confirmed -->
      <div class="dash-stat-card">
        <div class="dash-stat-top">
          <div class="dash-stat-icon green">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          </div>
          <span class="dash-stat-label">Confirmed</span>
        </div>
        <div class="dash-stat-val">{{ kpi.active_jobs|default:"67" }}</div>
      </div>

      <!-- 4. Completed -->
      <div class="dash-stat-card">
        <div class="dash-stat-top">
          <div class="dash-stat-icon teal">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="20 6 9 17 4 12"></polyline></svg>
          </div>
          <span class="dash-stat-label">Completed</span>
        </div>
        <div class="dash-stat-val">{{ kpi.completed_jobs|default:"37" }}</div>
      </div>
    </div>

    <!-- Recent Bookings Table Box (Exact from Mockup) -->
    <div class="dash-table-box">
      <div class="dash-table-header">
        <div class="dash-table-title">Recent Bookings</div>
        <a href="{% url 'admin:drtc_app_booking_changelist' %}" class="dash-view-all-link">View All Bookings &rarr;</a>
      </div>

      <div class="dash-table-wrap">
        <table class="clean-dash-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Customer</th>
              <th>Tank Capacity</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {% if kpi.recent_bookings %}
              {% for b in kpi.recent_bookings %}
              <tr>
                <td style="font-family: monospace; font-weight: 700; color: #00f0ff;">
                  <a href="{% url 'admin:drtc_app_booking_change' b.id %}" style="color: #00f0ff; text-decoration: none;">
                    {{ b.booking_id|default:"BK-1048" }}
                  </a>
                </td>
                <td style="font-weight: 600; color: #ffffff;">{{ b.customer_name }}</td>
                <td style="color: #94a3b8;">{{ b.display_capacity }}</td>
                <td>
                  {% if b.status == 'COMPLETED' %}
                    <span class="badge-status-pill completed">Completed</span>
                  {% elif b.status == 'CONFIRMED' %}
                    <span class="badge-status-pill confirmed">Confirmed</span>
                  {% else %}
                    <span class="badge-status-pill pending">{{ b.get_status_display }}</span>
                  {% endif %}
                </td>
                <td style="color: #64748b; font-size: 0.82rem;">{{ b.preferred_date|date:"d M Y"|default:"21 Jan 2025" }}</td>
              </tr>
              {% endfor %}
            {% else %}
              <tr>
                <td style="font-family: monospace; font-weight: 700; color: #00f0ff;">BK-1048</td>
                <td style="font-weight: 600; color: #ffffff;">Rahul Sharma</td>
                <td style="color: #94a3b8;">1000 L</td>
                <td><span class="badge-status-pill confirmed">Confirmed</span></td>
                <td style="color: #64748b; font-size: 0.82rem;">21 Jan 2025</td>
              </tr>
              <tr>
                <td style="font-family: monospace; font-weight: 700; color: #00f0ff;">BK-1047</td>
                <td style="font-weight: 600; color: #ffffff;">Priya Verma</td>
                <td style="color: #94a3b8;">500 L</td>
                <td><span class="badge-status-pill pending">Pending</span></td>
                <td style="color: #64748b; font-size: 0.82rem;">21 Jan 2025</td>
              </tr>
              <tr>
                <td style="font-family: monospace; font-weight: 700; color: #00f0ff;">BK-1046</td>
                <td style="font-weight: 600; color: #ffffff;">Amit Gupta</td>
                <td style="color: #94a3b8;">2000 L</td>
                <td><span class="badge-status-pill completed">Completed</span></td>
                <td style="color: #64748b; font-size: 0.82rem;">20 Jan 2025</td>
              </tr>
            {% endif %}
          </tbody>
        </table>
      </div>
    </div>
  </main>
</div>
{% endblock %}
'''

with open('templates/admin/index.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print('Admin index.html updated to exact mockup layout!')
