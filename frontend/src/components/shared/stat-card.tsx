import { Card, CardContent } from '@/components/ui/card'

export type StatCardColor = 'blue' | 'green' | 'yellow' | 'red' | 'purple'

interface StatCardProps {
  title: string
  value: number | string
  icon: React.ComponentType<{ size?: number }>
  color: StatCardColor
  subtitle?: string
  size?: 'sm' | 'md' | 'lg'
}

const colorClasses: Record<StatCardColor, string> = {
  blue: 'bg-blue-100 text-blue-700',
  green: 'bg-green-100 text-green-700',
  yellow: 'bg-yellow-100 text-yellow-700',
  red: 'bg-red-100 text-red-700',
  purple: 'bg-purple-100 text-purple-700',
}

const sizeConfig = {
  sm: {
    padding: 'p-3 sm:p-4',
    gap: 'gap-2 sm:gap-3',
    iconPadding: 'p-1.5 sm:p-2',
    iconSize: 16,
    valueSize: 'text-xl sm:text-2xl',
    titleSize: 'text-xs sm:text-sm',
    subtitleSize: 'text-xs',
  },
  md: {
    padding: 'p-4 sm:p-6',
    gap: 'gap-3 sm:gap-4',
    iconPadding: 'p-2 sm:p-3',
    iconSize: 20,
    valueSize: 'text-2xl sm:text-3xl',
    titleSize: 'text-sm sm:text-base',
    subtitleSize: 'text-xs',
  },
  lg: {
    padding: 'p-6',
    gap: 'gap-4',
    iconPadding: 'p-3',
    iconSize: 24,
    valueSize: 'text-3xl',
    titleSize: 'text-base',
    subtitleSize: 'text-xs',
  },
}

export function StatCard({ 
  title, 
  value, 
  icon: Icon, 
  color,
  subtitle,
  size = 'md'
}: StatCardProps) {
  const config = sizeConfig[size]

  return (
    <Card>
      <CardContent className={config.padding}>
        <div className={`flex items-center ${config.gap}`}>
          <div className={`${config.iconPadding} rounded-lg ${colorClasses[color]}`}>
            <Icon size={config.iconSize} />
          </div>
          <div className="min-w-0 flex-1">
            <p className={`${config.valueSize} font-semibold`}>{value}</p>
            <p className={`${config.titleSize} text-muted-foreground truncate`}>{title}</p>
            {subtitle && (
              <p className={`${config.subtitleSize} text-muted-foreground truncate`}>
                {subtitle}
              </p>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 