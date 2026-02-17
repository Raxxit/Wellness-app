<template>
  <div class="resources-page">
    <!-- Header -->
    <header class="page-header">
      <div class="header-container">
        <div class="header-content">
          <h1 class="main-title">
            <span class="title-icon">🧠</span>
            Mental Wellness Resources
          </h1>
          <p class="subtitle">Curated collection of mental health support resources</p>
        </div>
      </div>
    </header>

    <!-- Emergency Banner -->
    <div class="emergency-banner">
      <div class="banner-container">
        <div class="banner-content">
          <div class="banner-icon">🆘</div>
          <div class="banner-text">
            <h3 class="banner-title">Emergency Support</h3>
            <p class="banner-description">If you're in crisis, contact these services immediately</p>
          </div>
        </div>
        <div class="emergency-numbers">
          <div class="number-card">
            <div class="number">+230 800 9393</div>
            <div class="number-label">Suicide & Crisis Lifeline (Befrienders Mauritius)</div>
          </div>
          <div class="number-card">
            <div class="number">999</div>
            <div class="number-label">Emergency Services (Police)</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Category Navigation -->
    <nav class="category-navigation">
      <div class="nav-container">
        <div class="nav-grid">
          <button v-for="category in categories" :key="category.id" class="category-card"
            :class="{ active: activeCategory === category.id }" @click="activeCategory = category.id">
            <div class="category-icon">{{ category.icon }}</div>
            <div class="category-name">{{ category.name }}</div>
            <div class="category-count">{{ getResourceCount(category.id) }} resources</div>
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <div class="content-container">

        <!-- Videos Section -->
        <section v-if="activeCategory === 'videos'" class="resource-section">
          <div class="section-header">
            <h2 class="section-title">
              <span class="section-icon">🎬</span>
              Educational Videos
            </h2>
            <p class="section-description">Learn through visual content and guided sessions</p>
          </div>
          <div class="resources-grid">
            <div v-for="video in videoResources" :key="video.id" class="resource-item">
              <div class="resource-icon">{{ video.icon }}</div>
              <h3 class="resource-title">{{ video.title }}</h3>
              <p class="resource-description">{{ video.description }}</p>
              <div class="resource-meta">
                <span class="meta-item">
                  <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  {{ video.duration }}
                </span>
                <span class="meta-item">
                  <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 20h9"></path>
                    <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                  </svg>
                  {{ video.level }}
                </span>
              </div>
              <a :href="video.link" target="_blank" class="resource-link">
                Watch Video
                <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>
        </section>

        <!-- Articles Section -->
        <section v-if="activeCategory === 'articles'" class="resource-section">
          <div class="section-header">
            <h2 class="section-title">
              <span class="section-icon">📚</span>
              Articles & Guides
            </h2>
            <p class="section-description">Research-based articles and practical guides</p>
          </div>
          <div class="resources-grid">
            <div v-for="article in articleResources" :key="article.id" class="resource-item">
              <div class="resource-icon">{{ article.icon }}</div>
              <h3 class="resource-title">{{ article.title }}</h3>
              <p class="resource-description">{{ article.description }}</p>
              <div class="resource-meta">
                <span class="meta-item">
                  <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  {{ article.readTime }}
                </span>
                <span class="meta-item">
                  <svg class="meta-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                  </svg>
                  Research-based
                </span>
              </div>
              <a :href="article.link" target="_blank" class="resource-link">
                Read Article
                <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>
        </section>

        <!-- Podcasts Section -->
        <section v-if="activeCategory === 'podcasts'" class="resource-section">
          <div class="section-header">
            <h2 class="section-title">
              <span class="section-icon">🎧</span>
              Mental Health Podcasts
            </h2>
            <p class="section-description">Listen and learn from mental health experts</p>
          </div>
          <div class="resources-grid">
            <div v-for="podcast in podcastResources" :key="podcast.id" class="resource-item">
              <div class="resource-icon">{{ podcast.icon }}</div>
              <h3 class="resource-title">{{ podcast.title }}</h3>
              <p class="resource-description">{{ podcast.description }}</p>
              <div class="platform-buttons">
                <a :href="podcast.spotify" target="_blank" class="platform-button spotify">
                  <svg class="platform-icon" viewBox="0 0 24 24">
                    <path
                      d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z" />
                  </svg>
                  Spotify
                </a>
                <a :href="podcast.apple" target="_blank" class="platform-button apple">
                  <svg class="platform-icon" viewBox="0 0 24 24">
                    <path
                      d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.31-2.33 1.05-3.11z" />
                  </svg>
                  Apple Podcasts
                </a>
              </div>
            </div>
          </div>
        </section>

        <!-- Apps Section -->
        <section v-if="activeCategory === 'apps'" class="resource-section">
          <div class="section-header">
            <h2 class="section-title">
              <span class="section-icon">📱</span>
              Wellness Apps
            </h2>
            <p class="section-description">Digital tools for daily mental wellness practice</p>
          </div>
          <div class="resources-grid">
            <div v-for="app in appResources" :key="app.id" class="resource-item">
              <div class="resource-icon">{{ app.icon }}</div>
              <h3 class="resource-title">{{ app.title }}</h3>
              <p class="resource-description">{{ app.description }}</p>
              <div class="feature-tags">
                <span v-for="feature in app.features" :key="feature" class="feature-tag">
                  {{ feature }}
                </span>
              </div>
              <a :href="app.link" target="_blank" class="resource-link">
                Visit App
                <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>
        </section>

        <!-- Websites Section -->
        <section v-if="activeCategory === 'websites'" class="resource-section">
          <div class="section-header">
            <h2 class="section-title">
              <span class="section-icon">🌐</span>
              Organizations & Websites
            </h2>
            <p class="section-description">Trusted mental health organizations and resources</p>
          </div>
          <div class="resources-grid">
            <div v-for="website in websiteResources" :key="website.id" class="resource-item">
              <div class="resource-icon">{{ website.icon }}</div>
              <h3 class="resource-title">{{ website.title }}</h3>
              <p class="resource-description">{{ website.description }}</p>
              <div class="service-badges">
                <span v-if="website.free" class="service-badge free">Free Resources</span>
                <span v-if="website.helpline" class="service-badge helpline">24/7 Helpline</span>
                <span v-if="website.education" class="service-badge education">Education</span>
              </div>
              <a :href="website.link" target="_blank" class="resource-link">
                Visit Website
                <svg class="link-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                  <polyline points="15 3 21 3 21 9"></polyline>
                  <line x1="10" y1="14" x2="21" y2="3"></line>
                </svg>
              </a>
            </div>
          </div>
        </section>

      </div>
    </main>

  </div>
</template>

<script>
export default {
  name: 'MentalWellnessResources',
  data() {
    return {
      activeCategory: 'videos',
      categories: [
        { id: 'videos', name: 'Videos', icon: '🎬' },
        { id: 'articles', name: 'Articles', icon: '📚' },
        { id: 'podcasts', name: 'Podcasts', icon: '🎧' },
        { id: 'apps', name: 'Apps', icon: '📱' },
        { id: 'websites', name: 'Websites', icon: '🌐' }
      ],
      videoResources: [
        {
          id: 1,
          icon: '🧘',
          title: 'Mindfulness Meditation',
          description: 'Guided meditation for stress reduction and mental clarity',
          duration: '15 min',
          level: 'Beginner',
          link: 'https://www.youtube.com/watch?v=ssss7V1_eyA'
        },
        {
          id: 2,
          icon: '😰',
          title: 'Understanding Anxiety',
          description: 'Learn about anxiety disorders and coping mechanisms',
          duration: '12 min',
          level: 'Intermediate',
          link: 'https://www.youtube.com/watch?v=WF7uFgJcUO0'
        },
        {
          id: 3,
          icon: '💭',
          title: 'CBT Techniques',
          description: 'Cognitive Behavioral Therapy for negative thought patterns',
          duration: '18 min',
          level: 'Intermediate',
          link: 'https://www.youtube.com/watch?v=WRRdSm4ZjX4'
        },
        {
          id: 4,
          icon: '😊',
          title: 'Emotional Resilience',
          description: 'Build mental strength and bounce back from setbacks',
          duration: '20 min',
          level: 'All Levels',
          link: 'https://www.youtube.com/watch?v=N9XKLmtNn1E'
        }
      ],
      articleResources: [
        {
          id: 1,
          icon: '📖',
          title: 'Mental Health First Aid',
          description: 'How to support someone experiencing mental health issues',
          readTime: '10 min read',
          link: 'https://www.mentalhealthfirstaid.org/'
        },
        {
          id: 2,
          icon: '😴',
          title: 'Sleep & Mental Health',
          description: 'The connection between sleep quality and emotional well-being',
          readTime: '8 min read',
          link: 'https://www.sleepfoundation.org/mental-health'
        },
        {
          id: 3,
          icon: '🥦',
          title: 'Nutrition for Wellness',
          description: 'How diet affects mood, anxiety, and brain function',
          readTime: '12 min read',
          link: 'https://www.health.harvard.edu/blog/nutritional-psychiatry-your-brain-on-food-201511168626'
        },
        {
          id: 4,
          icon: '🏃',
          title: 'Exercise for Depression',
          description: 'Evidence-based benefits of physical activity for mental health',
          readTime: '7 min read',
          link: 'https://www.apa.org/monitor/2011/12/exercise'
        }
      ],
      podcastResources: [
        {
          id: 1,
          icon: '😊',
          title: 'The Happiness Lab',
          description: 'Science-based approaches to happiness with Dr. Laurie Santos',
          spotify: 'https://open.spotify.com/show/3oUz1BDVEI2tQQHcV+w8H9',
          apple: 'https://podcasts.apple.com/us/podcast/the-happiness-lab-with-dr-laurie-santos/id1474245040'
        },
        {
          id: 2,
          icon: '💬',
          title: 'Mental Illness Happy Hour',
          description: 'Honest conversations about mental health struggles and recovery',
          spotify: 'https://open.spotify.com/show/4kHZ2kKTqCxBmtq0CQKbF7',
          apple: 'https://podcasts.apple.com/us/podcast/the-mental-illness-happy-hour/id398713431'
        },
        {
          id: 3,
          icon: '🎭',
          title: 'Terrible, Thanks for Asking',
          description: 'Real talk about the hard things people are going through',
          spotify: 'https://open.spotify.com/show/5cUd3q8QHtLr6HhZ3fSfkB',
          apple: 'https://podcasts.apple.com/us/podcast/terrible-thanks-for-asking/id1176893299'
        },
        {
          id: 4,
          icon: '🧠',
          title: 'The Psychology Podcast',
          description: 'Exploring the mysteries of the human mind with experts',
          spotify: 'https://open.spotify.com/show/5dlKxYy9SdUz9OcCQJz75I',
          apple: 'https://podcasts.apple.com/us/podcast/the-psychology-podcast/id955080169'
        }
      ],
      appResources: [
        {
          id: 1,
          icon: '🧘',
          title: 'Headspace',
          description: 'Meditation and mindfulness app with guided sessions',
          features: ['Meditation', 'Sleep', 'Focus'],
          link: 'https://www.headspace.com/'
        },
        {
          id: 2,
          icon: '🌊',
          title: 'Calm',
          description: 'Sleep stories, meditations, and relaxation music',
          features: ['Sleep', 'Meditation', 'Music'],
          link: 'https://www.calm.com/'
        },
        {
          id: 3,
          icon: '📝',
          title: 'Moodfit',
          description: 'Mental fitness tools and mood tracking insights',
          features: ['Tracking', 'Insights', 'Tools'],
          link: 'https://www.getmoodfit.com/'
        },
        {
          id: 4,
          icon: '🤖',
          title: 'Woebot',
          description: 'AI-powered CBT chatbot for mental health support',
          features: ['CBT', 'Chatbot', 'Check-ins'],
          link: 'https://woebothealth.com/'
        }
      ],
      websiteResources: [
        {
          id: 1,
          icon: '🏛️',
          title: 'NAMI',
          description: 'National Alliance on Mental Illness - advocacy and support',
          free: true,
          helpline: true,
          education: true,
          link: 'https://www.nami.org/'
        },
        {
          id: 2,
          icon: '🩺',
          title: 'Mental Health America',
          description: 'Community-based nonprofit promoting mental health awareness',
          free: true,
          helpline: true,
          education: true,
          link: 'https://www.mhanational.org/'
        },
        {
          id: 3,
          icon: '🌍',
          title: 'WHO Mental Health',
          description: 'Global mental health resources and statistics',
          free: true,
          helpline: false,
          education: true,
          link: 'https://www.who.int/health-topics/mental-health'
        },
        {
          id: 4,
          icon: '🎓',
          title: 'American Psychological Association',
          description: 'Professional organization with mental health resources',
          free: false,
          helpline: false,
          education: true,
          link: 'https://www.apa.org/topics'
        }
      ]
    }
  },
  methods: {
    getResourceCount(categoryId) {
      const counts = {
        'videos': this.videoResources.length,
        'articles': this.articleResources.length,
        'podcasts': this.podcastResources.length,
        'apps': this.appResources.length,
        'websites': this.websiteResources.length
      }
      return counts[categoryId] || 0
    }
  }
}
</script>

<style scoped>
/* Base Styles */
.resources-page {
  min-height: 100vh;
  background: #f8fafc;
  color: #1e293b;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Header */
.page-header {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  padding: 3rem 0 2rem;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.header-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.main-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.title-icon {
  font-size: 2.75rem;
}

.subtitle {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.header-notes {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.note-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  font-size: 0.875rem;
}

.note-icon {
  font-size: 1rem;
}

/* Emergency Banner */
.emergency-banner {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  margin: 1.5rem auto;
  border-radius: 16px;
  overflow: hidden;
  max-width: 1200px;
  box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.2);
}

.banner-container {
  padding: 1.5rem;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.banner-icon {
  font-size: 2.5rem;
}

.banner-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.banner-description {
  opacity: 0.9;
  font-size: 0.875rem;
}

.emergency-numbers {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.number-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 1.25rem;
  border-radius: 12px;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: transform 0.2s ease;
}

.number-card:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.15);
}

.number {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.number-label {
  font-size: 0.875rem;
  opacity: 0.9;
}

/* Category Navigation */
.category-navigation {
  padding: 2rem 0;
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}

.category-card {
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.category-card:hover {
  border-color: #c7d2fe;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
}

.category-card.active {
  background: #6366f1;
  border-color: #6366f1;
  color: white;
}

.category-card.active .category-count {
  background: rgba(255, 255, 255, 0.2);
}

.category-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

.category-name {
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.category-count {
  background: #e2e8f0;
  color: #64748b;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Main Content */
.main-content {
  padding: 3rem 0;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.resource-section {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.875rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.section-icon {
  font-size: 2rem;
}

.section-description {
  color: #64748b;
  font-size: 1.125rem;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Resources Grid */
.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.resource-item {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.resource-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border-color: #c7d2fe;
}

.resource-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.resource-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #1e293b;
}

.resource-description {
  color: #64748b;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  flex-grow: 1;
}

/* Resource Meta */
.resource-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.25rem;
  font-size: 0.75rem;
  color: #64748b;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.meta-icon {
  width: 12px;
  height: 12px;
  stroke-width: 2;
}

/* Links */
.resource-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #6366f1;
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s ease;
  margin-top: auto;
}

.resource-link:hover {
  background: #4f46e5;
  transform: translateY(-1px);
}

.link-icon {
  width: 16px;
  height: 16px;
  stroke-width: 2;
}

/* Platform Buttons */
.platform-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: auto;
}

.platform-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  flex: 1;
  padding: 0.75rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.platform-button.spotify {
  background: #1db954;
  color: white;
}

.platform-button.apple {
  background: #a2aaad;
  color: white;
}

.platform-button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.platform-icon {
  width: 16px;
  height: 16px;
}

/* Feature Tags */
.feature-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.feature-tag {
  background: #f1f5f9;
  color: #475569;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

/* Service Badges */
.service-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.service-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
}

.service-badge.free {
  background: #dcfce7;
  color: #166534;
}

.service-badge.helpline {
  background: #fef3c7;
  color: #92400e;
}

.service-badge.education {
  background: #e0e7ff;
  color: #3730a3;
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-title {
    font-size: 2rem;
    flex-direction: column;
    gap: 0.5rem;
  }

  .title-icon {
    font-size: 2.25rem;
  }

  .section-title {
    font-size: 1.5rem;
    flex-direction: column;
    gap: 0.5rem;
  }

  .nav-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .resources-grid {
    grid-template-columns: 1fr;
  }

  .emergency-numbers {
    grid-template-columns: 1fr;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

@media (max-width: 480px) {
  .header-notes {
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

  .nav-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    margin-bottom: 2rem;
  }

  .resource-item {
    padding: 1.25rem;
  }
}
</style>